import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras import layers
from ConcurrencyDetectorEnvironment import ConcurrencyDetectorEnvironment
import utils

# thread name, parent arr, var name, mutex name
siccl_example_flattened = np.array([[1, 0, 2, 0],
                                    [1, 0, 3, 0],
                                    [5, 1, 2, 0], 
                                    [5, 1, 3, 0], 
                                    [6, 5, 2, 0], 
                                    [6, 5, 3, 0], 
                                    [7, 5, 2, 0]], dtype=int)

# siccl_example_flattened = np.array([[ 1,  0,  2,  0],
#                                    [ 2,  1,  9,  0],
#                                    [ 3,  2,  3,  0],
#                                    [ 3,  2,  4,  0],
#                                    [ 3,  2,  2,  0],
#                                    [ 3,  2,  6,  0],
#                                    [ 4,  3, 10,  0],
#                                    [ 4,  3,  1,  0],
#                                    [ 4,  3,  7,  0],
#                                    [ 4,  3,  9,  0],
#                                    [ 4,  3,  4,  0],
#                                    [ 5,  4,  3,  0],
#                                    [ 5,  4,  4,  0],
#                                    [ 5,  4, 10,  0],
#                                    [ 5,  4,  5,  0],
#                                    [ 5,  4,  9,  0],
#                                    [ 6,  5,  2,  0],
#                                    [ 6,  5,  4,  0],
#                                    [ 6,  5,  6,  0],
#                                    [ 6,  5,  6,  0],
#                                    [ 6,  5,  5,  0],
#                                    [ 7,  6,  6,  0],
#                                    [ 7,  6,  2,  0],
#                                    [ 8,  7,  9,  0],
#                                    [ 8,  7, 10,  0],
#                                    [ 8,  7,  9,  0],
#                                    [ 8,  7,  1,  0],
#                                    [ 8,  7,  1,  0],
#                                    [ 9,  8,  7,  0],
#                                    [ 9,  8,  4,  0],
#                                    [ 9,  8,  9,  0],
#                                    [10,  9,  1,  0],
#                                    [10,  9,  8,  0],
#                                    [10,  9,  2,  0],
#                                    [10,  9, 10,  0],
#                                    [11, 10,  2,  0],
#                                    [11, 10,  7,  0],
#                                    [11, 10,  3,  0],
#                                    [11, 10,  2,  0],
#                                    [11, 10,  6,  0],
#                                    [12, 11,  5,  0],
#                                    [12, 11,  9,  0],
#                                    [12, 11,  1,  0],
#                                    [12, 11,  6,  0],
#                                    [12, 11,  3,  0],
#                                    [13, 12,  6,  0],
#                                    [13, 12,  5,  0],
#                                    [13, 12, 10,  0],
#                                    [13, 12, 10,  0],
#                                    [14, 13,  1,  0],
#                                    [14, 13,  7,  0],
#                                    [14, 13,  8,  0],
#                                    [14, 13,  9,  0],
#                                    [14, 13,  1,  0],
#                                    [15, 14,  4,  0],
#                                    [15, 14,  9,  0],
#                                    [15, 14,  4,  0],
#                                    [16, 15,  3,  0],
#                                    [16, 15,  6,  0],
#                                    [16, 15,  6,  0],
#                                    [17, 16,  1,  0],
#                                    [17, 16, 10,  0],
#                                    [18, 17,  5,  0],
#                                    [18, 17,  1,  0],
#                                    [18, 17,  5,  0],
#                                    [18, 17,  9,  0],
#                                    [19, 18,  8,  0],
#                                    [19, 18,  7,  0],
#                                    [19, 18,  6,  0],
#                                    [19, 18,  7,  0],
#                                    [20, 19,  8,  0],
#                                    [20, 19,  7,  0],
#                                    [20, 19,  1,  0],
#                                    [20, 19,  3,  0],
#                                    [20, 19,  5,  0],
#                                    [21, 20,  3,  0],
#                                    [22, 21,  2,  0],
#                                    [22, 21,  4,  0],
#                                    [22, 21,  7,  0],
#                                    [23, 22,  2,  0],
#                                    [23, 22, 10,  0],
#                                    [23, 22,  4,  0],
#                                    [23, 22,  4,  0],
#                                    [23, 22,  9,  0],
#                                    [24, 23,  9,  0],
#                                    [24, 23,  9,  0],
#                                    [25, 24,  4,  0],
#                                    [25, 24,  6,  0],
#                                    [25, 24,  2,  0],
#                                    [25, 24,  1,  0],
#                                    [25, 24,  7,  0],
#                                    [26, 25,  8,  0],
#                                    [26, 25,  6,  0],
#                                    [26, 25,  2,  0],
#                                    [26, 25,  7,  0],
#                                    [26, 25,  6,  0],
#                                    [27, 26,  9,  0],
#                                    [28, 27,  7,  0],
#                                    [29, 28,  9,  0],
#                                    [30, 29,  8,  0],
#                                    [30, 29,  3,  0],
#                                    [30, 29,  4,  0],
#                                    [30, 29,  2,  0],], dtype=int)

# Configuration paramaters for the whole setup
gamma = 0.99  # Discount factor for past rewards
epsilon = 0.0001  # Epsilon greedy parameter
epsilon_min = 0.1  # Minimum epsilon greedy parameter
epsilon_max = 1.0  # Maximum epsilon greedy parameter
epsilon_interval = (
    epsilon_max - epsilon_min
)  # Rate at which to reduce chance of random action being taken
batch_size = 32  # Size of batch taken from replay buffer
max_steps_per_episode = 50000

n_indices = len(siccl_example_flattened)
n_mutexe = utils.count_unique(siccl_example_flattened[:, 2]) + 1 # 1 is for 0, so no mutex

env = ConcurrencyDetectorEnvironment(siccl_example_flattened, 1, 0.1)
eps = np.finfo(np.float32).eps.item()  # Smallest number such that 1.0 + eps != 1.0

def create_q_model():
    # Network defined by the Deepmind paper
    inputs = layers.Input(shape=(n_indices * 4))

    # Convolutions on the frames on the screen
    # layer1 = layers.Conv2D(32, 8, strides=4, activation="relu")(inputs)
    # layer2 = layers.Conv2D(64, 4, strides=2, activation="relu")(layer1)
    # layer3 = layers.Conv2D(64, 3, strides=1, activation="relu")(layer2)
    # layer4 = layers.Flatten()(layer3)

    layer1 = layers.Dense((n_indices*4), activation="relu")(inputs)
    layer2 = layers.Dense((n_indices*4)/2, activation="relu")(layer1)

    action_indices = layers.Dense(n_indices, activation="softmax")(layer2)
    action_mutex_id = layers.Dense(n_mutexe, activation="softmax")(layer2)

    return keras.Model(inputs=inputs, outputs=[action_indices, action_mutex_id])


# The first model makes the predictions for Q-values which are used to
# make a action.
model = create_q_model()
# Build a target model for the prediction of future rewards.
# The weights of a target model get updated every 10000 steps thus when the
# loss between the Q-values is calculated the target Q-value is stable.
model_target = create_q_model()


"""
## Train
"""
# In the Deepmind paper they use RMSProp however then Adam optimizer
# improves training time
optimizer = keras.optimizers.legacy.Adam(learning_rate=0.00025, clipnorm=1.0)
optimizert = keras.optimizers.legacy.Adam(learning_rate=0.00025, clipnorm=1.0)

# Experience replay buffers
action_history = []
absolute_atomic_err_rate_history = []
state_history = []
state_next_history = []
rewards_history = []
done_history = []
episode_reward_history = []
running_reward = 0
episode_count = 0
step_count = 0
# Number of frames to take random action and observe output
epsilon_random_frames = 5
# Number of frames for exploration
epsilon_greedy_frames = 100.0
# Maximum replay length
# Note: The Deepmind paper suggests 100.000.0 however this causes memory issues
max_memory_length = 100.000
# Train the model after 4 actions
update_after_actions = 4
# How often to update the target network
update_target_network = 10
# Using huber loss for stability
loss_function = keras.losses.Huber()

show_graph = 50

print(model.summary())
# print(model_target.summary())

while True:  # Run until solved
    state = siccl_example_flattened.flatten()
    action: list[int] = [0, 0]
    episode_reward = 0
    env.reset()
    print("reseted env")
    for timestep in range(1, max_steps_per_episode):
        step_count += 1

        # Use epsilon-greedy for exploration
        if step_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
            # Take random action
            action[0] = np.random.choice(n_indices)
            action[1] = np.random.choice(n_mutexe)
            print(str(epsilon), ">", str(np.random.rand(1)[0]))
        else:
            # Predict action Q-values
            # From environment state
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            indices_probs, mutexe_probs = model(state_tensor, training=False)

            action[0] = np.random.choice(a=n_indices, p=np.squeeze(indices_probs))
            action[1] = np.random.choice(a=n_mutexe, p=np.squeeze(mutexe_probs))
            print("action taken: ")
            print(action)
            # Take best action
            # indices_probs, mutexe_probs = tf.argmax(action_probs[0]).numpy()

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_frames
        epsilon = max(epsilon, epsilon_min)


        # Apply the sampled action in our environment
        state_next, reward, absolute_atomic_err_rate, done = env.step((action[0], action[1]))
        absolute_atomic_err_rate_history.append(absolute_atomic_err_rate)
        unflattened_state = state_next
        state_next = np.array(state_next).flatten()

        episode_reward += reward

        # Save actions and states in replay buffer
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        done_history.append(done)
        rewards_history.append(reward)
        state = state_next

        # Update every fourth frame and once batch size is over 32
        if step_count % update_after_actions == 0 and len(done_history) > batch_size:
            # Get indices of samples for replay buffers
            indices = np.random.choice(range(len(done_history)), size=batch_size)

            # Using list comprehension to sample from replay buffer
            state_sample = np.array([state_history[i] for i in indices])
            state_next_sample = np.array([state_next_history[i] for i in indices])
            rewards_sample = [rewards_history[i] for i in indices]
            action_sample_indices = [action_history[i][0] for i in indices]
            action_sample_mutexe = [action_history[i][1] for i in indices]
            done_sample = tf.convert_to_tensor([float(done_history[i]) for i in indices])

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = model_target.predict(state_next_sample)
            future_reward_indices = np.array(future_rewards[0])
            future_reward_mutexe = np.array(future_rewards[1])
            # print(reward_mutexe.shape)
            # print(reward_indices.shape)
            # Q value = reward + discount factor * expected future reward
            updated_q_values_indices = rewards_sample + gamma * tf.reduce_max(future_reward_indices, axis=1)
            updated_q_values_mutexe = rewards_sample + gamma * tf.reduce_max(future_reward_mutexe, axis=1)

            # If final frame set the last value to -1
            updated_q_values_indices = updated_q_values_indices * (1 - done_sample) - done_sample
            updated_q_values_mutexe = updated_q_values_mutexe * (1 - done_sample) - done_sample

            print(updated_q_values_indices, updated_q_values_mutexe)

            # Create a mask so we only calculate loss on the updated Q-values
            masks_indices = tf.one_hot(action_sample_indices, n_indices)
            masks_mutexe = tf.one_hot(action_sample_mutexe, n_mutexe)

            with tf.GradientTape() as tape_indices:
                # Train the model on the states and updated Q-values
                q_values_indices, q_values_mutexe = model(state_sample)

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action_indices = tf.reduce_sum(tf.multiply(q_values_indices, masks_indices), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss_indices = loss_function(updated_q_values_indices, q_action_indices)

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action_mutexe = tf.reduce_sum(tf.multiply(q_values_mutexe, masks_mutexe), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss_mutexe = loss_function(updated_q_values_mutexe, q_action_mutexe)

            # Backpropagation
            grads = tape_indices.gradient([loss_indices, loss_mutexe], model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))



        if step_count % show_graph == 0:
            figure, (plt1) = plt.subplots(1)
            plt1.plot(absolute_atomic_err_rate_history, label='absolute_atomic_err_rate')
            plt1.plot(rewards_history, label='rewards_history')
            plt1.legend(loc="upper right")
            plt.show()
            print("state:")
            print(unflattened_state)

        if step_count % update_target_network == 0:
            # update the the target network with new weights
            model_target.set_weights(model.get_weights())
            # Log details
            template = "running reward: {:.2f} at episode {}, frame count {}"
            print(template.format(running_reward, episode_count, step_count))

            
            # plt2.plot(action_probs_history, label='action_probs_history')
            # plt2.plot(critic_value_history, label='critic_value_history')
            # plt2.legend(loc="upper right")

            # plt3.plot(loss_history, label='loss_history')
            # plt3.legend(loc="upper right")

        # Limit the state and reward history
        if len(rewards_history) > max_memory_length:
            del rewards_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]

        if done:
            break

    # Update running reward to check condition for solving
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 100:
        del episode_reward_history[:1]
    running_reward = np.mean(episode_reward_history)

    episode_count += 1

    if running_reward > 40:  # Condition to consider the task solved
        print("Solved at episode {}!".format(episode_count))
        break