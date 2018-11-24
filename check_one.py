import os
import sys
import glob

import tensorflow as tf

import timeit

def predict(image_path, ret):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # change this as you see fit
    tot_sc = 0
    ret=[]
    al_sc = 0
    # Read the images data
    image_data = tf.gfile.GFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip()
                               for line in tf.gfile.GFile("retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.GFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        avg_prediction_time = 0.0
        score_avg_dict = {}
        start_time = timeit.default_timer()

        predictions = sess.run(softmax_tensor,
             {'DecodeJpeg/contents:0': image_data})
        correct_label="NORMAL"
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        elapsed = timeit.default_timer() - start_time
        avg_prediction_time += float(elapsed)
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if human_string not in score_avg_dict:
                score_avg_dict[human_string] = 0
            score_avg_dict[human_string] += score
            print( human_string, score)
     #   return ret

if __name__ == '__main__':
    ret=[]
    predict(sys.argv[1], ret)
