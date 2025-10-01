import os
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.core.protobuf import saver_pb2
import driving_data
import model

LOGDIR = './save'

sess = tf.InteractiveSession()

L2NormConst = 0.001

train_vars = tf.trainable_variables()

loss = tf.reduce_mean(tf.square(tf.subtract(model.y_, model.y))) + tf.add_n([tf.nn.l2_loss(v) for v in train_vars]) * L2NormConst
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

# Initialize variables
sess.run(tf.global_variables_initializer())

# Try to restore from checkpoint if it exists
checkpoint_path = os.path.join(LOGDIR, "model.ckpt")
if os.path.exists(checkpoint_path + ".index"):
    print("Loading existing model from checkpoint...")
    saver = tf.train.Saver(write_version = saver_pb2.SaverDef.V2)
    saver.restore(sess, checkpoint_path)
    print("Model restored successfully!")
else:
    print("No existing checkpoint found, starting with fresh model.")
    saver = tf.train.Saver(write_version = saver_pb2.SaverDef.V2)

# create summaries to monitor training and validation loss tensors
train_loss_summary = tf.summary.scalar("train_loss", loss)
val_loss_summary = tf.summary.scalar("val_loss", loss)
# merge all summaries into a single op
merged_summary_op = tf.summary.merge_all()

# op to write logs to Tensorboard
logs_path = './logs'
summary_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())

epochs = 50
batch_size = 64

# train over the dataset about 30 times
for epoch in range(epochs):
  for i in range(int(driving_data.num_images/batch_size)):
    xs, ys = driving_data.LoadTrainBatch(batch_size)
    train_step.run(feed_dict={model.x: xs, model.y_: ys, model.keep_prob: 0.8})

    # compute and log training loss
    train_loss_value, train_loss_summ = sess.run([loss, train_loss_summary], feed_dict={model.x: xs, model.y_: ys, model.keep_prob: 1.0})
    summary_writer.add_summary(train_loss_summ, epoch * driving_data.num_images/batch_size + i)

    if i % 10 == 0:
      xs_val, ys_val = driving_data.LoadValBatch(batch_size)
      val_loss_value, val_loss_summ = sess.run([loss, val_loss_summary], feed_dict={model.x: xs_val, model.y_: ys_val, model.keep_prob: 1.0})
      print("Epoch: %d, Step: %d, Train Loss: %g, Val Loss: %g" % (epoch, epoch * batch_size + i, train_loss_value, val_loss_value))
      summary_writer.add_summary(val_loss_summ, epoch * driving_data.num_images/batch_size + i)

    if i % batch_size == 0:
      if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
      checkpoint_path = os.path.join(LOGDIR, "model.ckpt")
      filename = saver.save(sess, checkpoint_path)
  print("Model saved in file: %s" % filename)

print("Run the command line:\n" \
      "--> tensorboard --logdir=./logs " \
      "\nThen open http://0.0.0.0:6006/ into your web browser")
