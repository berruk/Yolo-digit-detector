# -*- coding: utf-8 -*-

from keras.layers import Input

from yolo.decoder import YoloDecoder
from yolo.loss import YoloLoss
from yolo.trainer import YoloTrainer
from yolo.preprocessing import GeneratorConfig

# create_feature_extractor(architecture, input_size)
# client : predict.py
# client : train.py
class YOLO(object):
    def __init__(self, network,
                       labels, 
                       anchors):
        """
        # Args
            feature_extractor : BaseFeatureExtractor instance
        """
        self._yolo_network = network
        self._yolo_network = network
        self._yolo_network = network
        self._yolo_network = network
        
        
        
        self.labels   = list(labels)
        self.nb_class = len(self.labels)
        self.anchors  = anchors

        # print a summary of the whole model
        self._yolo_network.model.summary()

    def load_weights(self, weight_path):
        self._yolo_network.load_weights(weight_path)

    def predict(self, image):
        """
        # Args
            image : 3d-array
        
        # Returns
            boxes : list of BoundBox instance
        """
        netout = self._yolo_network.forward(image)
        yolo_decoder = YoloDecoder(self.anchors)
        boxes = yolo_decoder.run(netout)
        return boxes

    def train(self, train_imgs,     # the list of images to train the model
                    valid_imgs,     # the list of images used to validate the model
                    train_times,    # the number of time to repeat the training set, often used for small datasets
                    valid_times,    # the number of times to repeat the validation set, often used for small datasets
                    nb_epoch,       # number of epoches
                    learning_rate,  # the learning rate
                    batch_size,     # the size of the batch
                    warmup_epochs,  # number of initial batches to let the model familiarize with the new dataset
                    saved_weights_name='best_weights.h5',
                    debug=False):     

        warmup_bs  = warmup_epochs * (train_times*(len(train_imgs)/batch_size+1) + valid_times*(len(valid_imgs)/batch_size+1))
        yolo_loss = YoloLoss(self._yolo_network.grid_size,
                             self._yolo_network.grid_size,
                             batch_size,
                             self.anchors,
                             self._yolo_network.nb_box,
                             self.nb_class,
                             warmup_bs,
                             self._yolo_network.true_boxes)
        
        generator_config = GeneratorConfig(self._yolo_network.input_size,
                                           self._yolo_network.grid_size,
                                           self._yolo_network.nb_box,
                                           self.labels,
                                           batch_size,
                                           self._yolo_network.max_box_per_image,
                                           self.anchors)

        # YoloNetwork, YoloTrainer, YoloLoss
        
        # 1. Batch Generator 를 여기서 생성
        
        # 2. 
        
        # Todo : self.model.model 정리
        yolo_trainer = YoloTrainer(self._yolo_network.model,
                                   yolo_loss.custom_loss,
                                   self._yolo_network._feature_extractor.normalize,
                                   generator_config)
        yolo_trainer.train(train_imgs,
                           valid_imgs,
                           train_times,
                           valid_times,
                           nb_epoch,
                           learning_rate,
                           warmup_epochs,
                           saved_weights_name)
