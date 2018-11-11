import tensorflow as tf
import configparser
from util import log_util
from util import fn_util
import os


class Network:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        self.__init_hyper_param()

        self.cost = None
        self.train_step = None
        self.accuracy = None

    def __init_hyper_param(self):
        self.model_name = self.config.get("Model", "name")
        self.batch_size = self.config.getint("Dataset", "batch_size")
        self.repeat = self.config.getint("Dataset", "repeat_time")

        self.learning_rate = self.config.getfloat("Hyper Parameters", "learning_rate")
        self.echo = self.config.getint("Hyper Parameters", "echo")
        self.type = self.config.get("Hyper Parameters", "type")
        self.log_dir = self.config.get("Hyper Parameters", "log_dir") + self.model_name + "/log/"
        self.loss_fn = self.config.get("Hyper Parameters", "loss_fn")
        self.opt_fn = self.config.get("Hyper Parameters", "opt_fn")
        self.acc_fn = self.config.get("Hyper Parameters", "acc_fn")
        self.model_dir = self.config.get("Hyper Parameters", "model_dir") + self.model_name + "/ckp/"
        self.tensorboard_summary_enabled = self.config.get("Hyper Parameters", "enable_tensorboard_log")

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = log_util.get_file_logger(self.model_name, self.log_dir + self.model_name + ".txt")

    def _init_network(self):
        pass

    def _var_summaries(self, var):
        with tf.name_scope("Summaries"):
            mean = tf.reduce_mean(var)
            tf.summary.scalar("mean", mean)
            with tf.name_scope("stddev"):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar("stddev", stddev)
            tf.summary.scalar("max", tf.reduce_max(var))
            tf.summary.scalar("min", tf.reduce_min(var))
            tf.summary.histogram("histogram", var)

    def _add_train_ops(self):
        with tf.name_scope("Loss"):
            with tf.name_scope(self.loss_fn):
                self.cost = fn_util.get_loss_fn(self.loss_fn, self.y_, self.network)
                tf.summary.scalar(self.loss_fn, self.cost)
        with tf.name_scope("Train_Step"):
            optimizer = fn_util.get_opt_fn(self.opt_fn)
            self.train_step = optimizer(self.learning_rate).minimize(self.cost)
        with tf.name_scope("Accuracy"):
            self.accuracy = fn_util.get_acc_fn(self.acc_fn, self.y_, self.network)

    def train(self):
        pass

    def eval(self):
        pass

    def predict(self):
        pass


class ModelNotTrained(Exception):
    def __init__(self):
        print("Model is not trained yet")