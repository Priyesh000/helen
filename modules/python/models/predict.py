import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from modules.python.models.dataloader_predict import SequenceDataset
from modules.python.TextColor import TextColor
from tqdm import tqdm
import numpy as np
from modules.python.models.ModelHander import ModelHandler
from modules.python.Options import ImageSizeOptions, TrainOptions
from modules.python.DataStore import DataStore
"""
This script implements the predict method that is used by the call consensus method.

The algorithm is described here:

  1) INPUTS:
    - directory path to the image files generated by MarginPolish
    - model path directing to a trained model
    - batch size for minibatch prediction
    - num workers for minibatch processing threads
    - output directory path to where the output hdf5 will be saved
    - gpu mode indicating if GPU will be used
  2) METHOD:
    - Call predict function that loads the neural network and generates base predictions and saves it into a hdf5 file
        - Loads the model
        - Iterates over the input images in minibatch
        - For each image uses a sliding window method to slide of the image sequence
        - Aggregate the predictions to get sequence prediction for the entire image sequence
        - Save all the predictions to a file
  3) OUTPUT:
    - A hdf5 file containing all the base predictions   
"""


def predict(test_file, output_filename, model_path, batch_size, num_workers, threads, gpu_mode):
    """
    The predict method loads images generated by MarginPolish and produces base predictions using a
    sequence transduction model based deep neural network. This method loads the model and iterates over
    minibatch images to generate the predictions and saves the predictions to a hdf5 file.

    :param test_file: File to predict on
    :param output_filename: Name and path to the output file
    :param batch_size: Batch size used for minibatch prediction
    :param model_path: Path to a trained model
    :param gpu_mode: If true, predictions will be done over GPU
    :param num_workers: Number of workers to be used by the dataloader
    :param threads: Number of threads to use with pytorch
    :return: Prediction dictionary
    """
    # create the output hdf5 file where all the predictions will be saved
    prediction_data_file = DataStore(output_filename, mode='w')
    torch.set_num_threads(threads)
    sys.stderr.write(TextColor.GREEN + 'INFO: TORCH THREADS SET TO: ' + str(torch.get_num_threads()) + ".\n"
                     + TextColor.END)

    # notify that the process has started and loading data
    sys.stderr.write(TextColor.PURPLE + 'Loading data\n' + TextColor.END)

    # create a pytorch dataset and dataloader that loads the data in mini_batches
    test_data = SequenceDataset(test_file)
    test_loader = DataLoader(test_data,
                             batch_size=batch_size,
                             shuffle=False,
                             num_workers=num_workers)

    # load the model using the model path
    transducer_model_base, transducer_model_rle, epochs = ModelHandler.load_simple_model(model_path)

    # set the model to evaluation mode.
    transducer_model_base.eval()
    transducer_model_rle.eval()

    # if gpu mode is True, then load the model in the GPUs
    if gpu_mode:
        transducer_model_base = torch.nn.DataParallel(transducer_model_base).cuda()
        transducer_model_rle = torch.nn.DataParallel(transducer_model_rle).cuda()

    # notify that the model has loaded successfully
    sys.stderr.write(TextColor.CYAN + 'MODEL LOADED\n')

    # iterate over the data in minibatches
    with torch.no_grad():
        # the dataloader loop, iterates in minibatches. tqdm is the progress logger.
        for contig, contig_start, contig_end, chunk_id, base_image, rle_image, position, filename in tqdm(test_loader, ncols=50):
            # the images are usually in uint8, convert them to FloatTensor
            base_image = base_image.type(torch.FloatTensor)
            rle_image = rle_image.type(torch.FloatTensor)

            # initialize the hidden input for the first chunk
            hidden = torch.zeros(base_image.size(0), 2 * TrainOptions.GRU_LAYERS, TrainOptions.HIDDEN_SIZE)
            hidden_rle_a = torch.zeros(rle_image.size(0), 2 * TrainOptions.RLE_GRU_LAYERS, TrainOptions.RLE_HIDDEN_SIZE)
            hidden_rle_c = torch.zeros(rle_image.size(0), 2 * TrainOptions.RLE_GRU_LAYERS, TrainOptions.RLE_HIDDEN_SIZE)
            hidden_rle_g = torch.zeros(rle_image.size(0), 2 * TrainOptions.RLE_GRU_LAYERS, TrainOptions.RLE_HIDDEN_SIZE)
            hidden_rle_t = torch.zeros(rle_image.size(0), 2 * TrainOptions.RLE_GRU_LAYERS, TrainOptions.RLE_HIDDEN_SIZE)
            hidden_rle_combined = torch.zeros(rle_image.size(0), 2 * TrainOptions.RLE_GRU_LAYERS, TrainOptions.RLE_HIDDEN_SIZE)

            # if gpu_mode is True, transfer the image and hidden tensors to the GPU
            if gpu_mode:
                base_image = base_image.cuda()
                rle_image = rle_image.cuda()
                hidden = hidden.cuda()
                hidden_rle_a = hidden_rle_a.cuda()
                hidden_rle_c = hidden_rle_c.cuda()
                hidden_rle_g = hidden_rle_g.cuda()
                hidden_rle_t = hidden_rle_t.cuda()
                hidden_rle_combined = hidden_rle_combined.cuda()

            # this is a multi-task neural network where we predict a base and a run-length. We use two dictionaries
            # to keep track of predictions.
            # these two dictionaries save predictions for each of the chunks and later we aggregate all the predictions
            # over the entire sequence to get a sequence prediction for the whole sequence.
            prediction_base_tensor = torch.zeros((base_image.size(0), base_image.size(1), ImageSizeOptions.TOTAL_BASE_LABELS))
            prediction_rle_tensor = torch.zeros((rle_image.size(0), rle_image.size(2), ImageSizeOptions.TOTAL_RLE_LABELS))

            if gpu_mode:
                prediction_base_tensor = prediction_base_tensor.cuda()
                prediction_rle_tensor = prediction_rle_tensor.cuda()

            # now the images usually contain 1000 bases, we iterate on a sliding window basis where we process
            # the window size then jump to the next window
            for i in range(0, ImageSizeOptions.SEQ_LENGTH, TrainOptions.WINDOW_JUMP):
                # if current position + window size goes beyond the size of the window, that means we've reached the end
                if i + TrainOptions.TRAIN_WINDOW > ImageSizeOptions.SEQ_LENGTH:
                    break
                chunk_start = i
                chunk_end = i + TrainOptions.TRAIN_WINDOW

                # get the image chunk
                base_image_chunk = base_image[:, i:i+TrainOptions.TRAIN_WINDOW]
                rle_image_chunk = rle_image[:, :, i:i+TrainOptions.TRAIN_WINDOW]

                # get the base inference from the model
                base_out, hidden = transducer_model_base(base_image_chunk, hidden)
                rle_out, hidden_rle_a, hidden_rle_c, hidden_rle_g, hidden_rle_t, hidden_rle_combined = \
                    transducer_model_rle(rle_image_chunk, base_out, hidden_rle_combined, hidden_rle_a,
                                         hidden_rle_c, hidden_rle_g, hidden_rle_t)

                # now calculate how much padding is on the top and bottom of this chunk so we can do a simple
                # add operation
                top_zeros = chunk_start
                bottom_zeros = ImageSizeOptions.SEQ_LENGTH - chunk_end

                # we run a softmax a padding to make the output tensor compatible for adding
                inference_layers = nn.Sequential(
                    nn.Softmax(dim=2),
                    nn.ZeroPad2d((0, 0, top_zeros, bottom_zeros))
                )
                if gpu_mode:
                    inference_layers = inference_layers.cuda()

                # run the softmax and padding layers
                base_prediction = inference_layers(base_out)
                rle_prediction = inference_layers(rle_out)

                # now simply add the tensor to the global counter
                prediction_base_tensor = torch.add(prediction_base_tensor, base_prediction)
                prediction_rle_tensor = torch.add(prediction_rle_tensor, rle_prediction)

            # all done now create a SEQ_LENGTH long prediction list
            prediction_base_tensor = prediction_base_tensor.cpu()
            prediction_rle_tensor = prediction_rle_tensor.cpu()

            base_values, base_labels = torch.max(prediction_base_tensor, 2)
            rle_values, rle_labels = torch.max(prediction_rle_tensor, 2)

            predicted_base_labels = base_labels.cpu().numpy()
            predicted_rle_labels = rle_labels.cpu().numpy()

            # go to each of the images and save the predictions to the file
            for i in range(base_image.size(0)):
                prediction_data_file.write_prediction(contig[i], contig_start[i], contig_end[i], chunk_id[i],
                                                      position[i], predicted_base_labels[i], predicted_rle_labels[i],
                                                      filename[i])
