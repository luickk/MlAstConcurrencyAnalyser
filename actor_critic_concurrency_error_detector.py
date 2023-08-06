import gym
import utils
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from ConcurrencyDetectorEnvironment import ConcurrencyDetectorEnvironment

num_hidden = 400

# thread name, parent arr, var name, mutex name
# siccl_example_flattened = np.array([[0, 1, 2, 0],
#                                     [0, 1, 3, 0],
#                                     [1, 5, 2, 0], 
#                                     [1, 5, 3, 0], 
#                                     [5, 6, 2, 0], 
#                                     [5, 6, 3, 0], 
#                                     [5, 7, 2, 0]], dtype=int)
siccl_example_flattened = np.array([[ 1,  0,  2,  0],
                                   [ 2,  1,  9,  0],
                                   [ 3,  2,  3,  0],
                                   [ 3,  2,  4,  0],
                                   [ 3,  2,  2,  0],
                                   [ 3,  2,  6,  0],
                                   [ 4,  3, 10,  0],
                                   [ 4,  3,  1,  0],
                                   [ 4,  3,  7,  0],
                                   [ 4,  3,  9,  0],
                                   [ 4,  3,  4,  0],
                                   [ 5,  4,  3,  0],
                                   [ 5,  4,  4,  0],
                                   [ 5,  4, 10,  0],
                                   [ 5,  4,  5,  0],
                                   [ 5,  4,  9,  0],
                                   [ 6,  5,  2,  0],
                                   [ 6,  5,  4,  0],
                                   [ 6,  5,  6,  0],
                                   [ 6,  5,  6,  0],
                                   [ 6,  5,  5,  0],
                                   [ 7,  6,  6,  0],
                                   [ 7,  6,  2,  0],
                                   [ 8,  7,  9,  0],
                                   [ 8,  7, 10,  0],
                                   [ 8,  7,  9,  0],
                                   [ 8,  7,  1,  0],
                                   [ 8,  7,  1,  0],
                                   [ 9,  8,  7,  0],
                                   [ 9,  8,  4,  0],
                                   [ 9,  8,  9,  0],
                                   [10,  9,  1,  0],
                                   [10,  9,  8,  0],
                                   [10,  9,  2,  0],
                                   [10,  9, 10,  0],
                                   [11, 10,  2,  0],
                                   [11, 10,  7,  0],
                                   [11, 10,  3,  0],
                                   [11, 10,  2,  0],
                                   [11, 10,  6,  0],
                                   [12, 11,  5,  0],
                                   [12, 11,  9,  0],
                                   [12, 11,  1,  0],
                                   [12, 11,  6,  0],
                                   [12, 11,  3,  0],
                                   [13, 12,  6,  0],
                                   [13, 12,  5,  0],
                                   [13, 12, 10,  0],
                                   [13, 12, 10,  0],
                                   [14, 13,  1,  0],
                                   [14, 13,  7,  0],
                                   [14, 13,  8,  0],
                                   [14, 13,  9,  0],
                                   [14, 13,  1,  0],
                                   [15, 14,  4,  0],
                                   [15, 14,  9,  0],
                                   [15, 14,  4,  0],
                                   [16, 15,  3,  0],
                                   [16, 15,  6,  0],
                                   [16, 15,  6,  0],
                                   [17, 16,  1,  0],
                                   [17, 16, 10,  0],
                                   [18, 17,  5,  0],
                                   [18, 17,  1,  0],
                                   [18, 17,  5,  0],
                                   [18, 17,  9,  0],
                                   [19, 18,  8,  0],
                                   [19, 18,  7,  0],
                                   [19, 18,  6,  0],
                                   [19, 18,  7,  0],
                                   [20, 19,  8,  0],
                                   [20, 19,  7,  0],
                                   [20, 19,  1,  0],
                                   [20, 19,  3,  0],
                                   [20, 19,  5,  0],
                                   [21, 20,  3,  0],
                                   [22, 21,  2,  0],
                                   [22, 21,  4,  0],
                                   [22, 21,  7,  0],
                                   [23, 22,  2,  0],
                                   [23, 22, 10,  0],
                                   [23, 22,  4,  0],
                                   [23, 22,  4,  0],
                                   [23, 22,  9,  0],
                                   [24, 23,  9,  0],
                                   [24, 23,  9,  0],
                                   [25, 24,  4,  0],
                                   [25, 24,  6,  0],
                                   [25, 24,  2,  0],
                                   [25, 24,  1,  0],
                                   [25, 24,  7,  0],
                                   [26, 25,  8,  0],
                                   [26, 25,  6,  0],
                                   [26, 25,  2,  0],
                                   [26, 25,  7,  0],
                                   [26, 25,  6,  0],
                                   [27, 26,  9,  0],
                                   [28, 27,  7,  0],
                                   [29, 28,  9,  0],
                                   [30, 29,  8,  0],
                                   [30, 29,  3,  0],
                                   [30, 29,  4,  0],
                                   [30, 29,  2,  0],
                                   [30, 29,  3,  0],
                                   [31, 30, 10,  0],
                                   [31, 30, 10,  0],
                                   [32, 31,  5,  0],
                                   [32, 31, 10,  0],
                                   [32, 31,  3,  0],
                                   [32, 31, 10,  0],
                                   [33, 32,  8,  0],
                                   [33, 32,  4,  0],
                                   [33, 32,  9,  0],
                                   [34, 33,  7,  0],
                                   [34, 33,  5,  0],
                                   [35, 34,  5,  0],
                                   [35, 34,  2,  0],
                                   [35, 34,  5,  0],
                                   [35, 34,  4,  0],
                                   [36, 35,  6,  0],
                                   [37, 36,  4,  0],
                                   [37, 36,  5,  0],
                                   [37, 36, 10,  0],
                                   [38, 37,  4,  0],
                                   [39, 38,  6,  0],
                                   [39, 38,  1,  0],
                                   [39, 38,  1,  0],
                                   [39, 38,  1,  0],
                                   [40, 39,  5,  0],
                                   [40, 39,  4,  0],
                                   [40, 39,  1,  0],
                                   [41, 40,  5,  0],
                                   [41, 40,  1,  0],
                                   [41, 40,  6,  0],
                                   [42, 41,  4,  0],
                                   [43, 42,  7,  0],
                                   [43, 42,  3,  0],
                                   [43, 42,  1,  0],
                                   [43, 42,  3,  0],
                                   [44, 43,  2,  0],
                                   [44, 43,  2,  0],
                                   [44, 43, 10,  0],
                                   [45, 44,  3,  0],
                                   [45, 44,  3,  0],
                                   [45, 44,  2,  0],
                                   [45, 44, 10,  0],
                                   [45, 44,  9,  0],
                                   [46, 45,  7,  0],
                                   [46, 45,  9,  0],
                                   [46, 45, 10,  0],
                                   [46, 45,  7,  0],
                                   [47, 46,  7,  0],
                                   [47, 46,  1,  0],
                                   [47, 46, 10,  0],
                                   [48, 47,  7,  0],
                                   [48, 47,  2,  0],
                                   [48, 47,  7,  0],
                                   [48, 47,  8,  0],
                                   [48, 47,  6,  0],
                                   [49, 48,  7,  0],
                                   [49, 48,  9,  0],
                                   [49, 48,  4,  0],
                                   [50, 49,  7,  0],
                                   [51, 50, 10,  0],
                                   [51, 50,  3,  0],
                                   [51, 50,  2,  0],
                                   [51, 50,  7,  0],
                                   [51, 50,  4,  0],
                                   [52, 51,  6,  0],
                                   [52, 51,  5,  0],
                                   [53, 52,  3,  0],
                                   [54, 53,  4,  0],
                                   [54, 53,  5,  0],
                                   [54, 53,  7,  0],
                                   [54, 53,  7,  0],
                                   [54, 53,  8,  0],
                                   [55, 54,  7,  0],
                                   [55, 54, 10,  0],
                                   [55, 54,  2,  0],
                                   [56, 55,  2,  0],
                                   [57, 56,  6,  0],
                                   [57, 56,  7,  0],
                                   [57, 56,  1,  0],
                                   [57, 56,  1,  0],
                                   [57, 56,  3,  0],
                                   [58, 57, 10,  0],
                                   [59, 58,  1,  0],
                                   [59, 58,  8,  0],
                                   [59, 58,  3,  0],
                                   [59, 58,  2,  0],
                                   [59, 58,  1,  0],
                                   [60, 59,  7,  0],
                                   [60, 59,  1,  0],
                                   [60, 59,  6,  0],
                                   [60, 59,  1,  0],
                                   [61, 60,  1,  0],
                                   [61, 60,  3,  0],
                                   [61, 60, 10,  0],
                                   [61, 60,  1,  0],
                                   [62, 61, 10,  0]], dtype=int)
n_indices = len(siccl_example_flattened)
n_mutexe = utils.count_unique(siccl_example_flattened[:, 2]) + 1 # 1 is for 0, so no mutex
gamma = 0.99  # Discount factor for past rewards
max_steps_per_episode = 10


env = ConcurrencyDetectorEnvironment(siccl_example_flattened, 1, 0.1)
eps = np.finfo(np.float32).eps.item()  # Smallest number such that 1.0 + eps != 1.0

inputs = layers.Input(shape=(n_indices * 4,))
common = layers.Dense(num_hidden, activation="relu")(inputs)

# action = layers.Dense(num_actions, activation="softmax")(common)
action_indices = layers.Dense(n_indices, activation="softmax")(common)
action_mutex_id = layers.Dense(n_mutexe, activation="softmax")(common)

critic = layers.Dense(1)(common)

model = keras.Model(inputs=inputs, outputs=[action_indices, action_mutex_id, critic])

"""
## Train
"""

optimizer = keras.optimizers.Adam(learning_rate=0.1)
huber_loss = keras.losses.Huber()
action_probs_ep_history = []
critic_value_ep_history = []
rewards_ep_history = []

absolute_atomic_err_rate_history = []
rewards_history = []
action_probs_history = []
critic_value_history = []
loss_history = []

running_reward = 0
episode_count = 0

print(model.summary())

while True:  # Run until solved
    state = env.reset().flatten()
    episode_reward = 0
    with tf.GradientTape() as tape:
        for timestep in range(1, max_steps_per_episode):
            state = tf.convert_to_tensor(state)
            state = tf.expand_dims(state, 0)

            # Predict action probabilities and estimated future rewards
            # from environment state

            indices_probs, mutexe_probs, critic_value = model(state)
            critic_value_ep_history.append(critic_value[0, 0])
            critic_value_history.append(critic_value[0, 0])

            # Sample action from action probability distribution

            # action = np.random.choice(a=num_actions, p=np.squeeze(action_probs))
            index = np.random.choice(a=n_indices, p=np.squeeze(indices_probs))
            mutex_id = np.random.choice(a=n_mutexe, p=np.squeeze(mutexe_probs))

            # adding average of multi action confidence to history
            action_probs_ep_history.append(tf.math.log(np.average([indices_probs[0, index], mutexe_probs[0, mutex_id]])))
            action_probs_history.append(tf.math.log(np.average([indices_probs[0, index], mutexe_probs[0, mutex_id]])))

            # print(index, mutex_id)
            # Apply the sampled action in our environment
            state, reward, absolute_atomic_err_rate, done = env.step((index, mutex_id))
            absolute_atomic_err_rate_history.append(absolute_atomic_err_rate)
            # print(state)
            state = state.flatten()
            rewards_ep_history.append(reward)
            rewards_history.append(reward)
            episode_reward += reward
            
            print("action: " + str((index, mutex_id)))
            # print("siccl arr: " + str(env.siccl_arr))
            if done:
                break

        # Update running reward to check condition for solving
        running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

        # Calculate expected value from rewards
        # - At each timestep what was the total reward received after that timestep
        # - Rewards in the past are discounted by multiplying them with gamma
        # - These are the labels for our critic
        returns = []
        discounted_sum = 0
        for r in rewards_ep_history[::-1]:
            discounted_sum = r + gamma * discounted_sum
            returns.insert(0, discounted_sum)

        # Normalize
        returns = np.array(returns)
        returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
        returns = returns.tolist()

        # Calculating loss values to update our network
        history = zip(action_probs_ep_history, critic_value_ep_history, returns)

        actor_losses = []
        critic_losses = []
        for log_prob, value, ret in history:
            # At this point in history, the critic estimated that we would get a
            # total reward = `value` in the future. We took an action with log probability
            # of `log_prob` and ended up recieving a total reward = `ret`.
            # The actor must be updated so that it predicts an action that leads to
            # high rewards (compared to critic's estimate) with high probability.
            diff = ret - value
            actor_losses.append(-log_prob * diff)  # actor loss

            # The critic must be updated so that it predicts a better estimate of
            # the future rewards.
            critic_losses.append(huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0)))

        # Backpropagation
        loss_value = sum(actor_losses) + sum(critic_losses)
        loss_history.append(loss_value)

        grads = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
        print("loss:", loss_value)
        # Clear the loss and reward history
        action_probs_ep_history.clear()
        critic_value_ep_history.clear()
        rewards_ep_history.clear()

    # Log details
    episode_count += 1
    if episode_count % 20 == 0:
        template = "running reward: {:.2f} at episode {}"
        figure, (plt1, plt2, plt3) = plt.subplots(3)
        plt1.plot(absolute_atomic_err_rate_history, label='absolute_atomic_err_rate')
        plt1.plot(rewards_history, label='rewards_history')
        plt1.legend(loc="upper right")
        
        plt2.plot(action_probs_history, label='action_probs_history')
        plt2.plot(critic_value_history, label='critic_value_history')
        plt2.legend(loc="upper right")

        plt3.plot(loss_history, label='loss_history')
        plt3.legend(loc="upper right")

        
        plt.show()
        print(template.format(running_reward, episode_count))

    if running_reward > 195:  # Condition to consider the task solved
        print("Solved at episode {}!".format(episode_count))
        break
