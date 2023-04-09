import gym
import utils
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from concurrency_detector_env import ConcurrencyDetectorEnvironment

n_max_mutex = 100
num_hidden = 128

num_actions = 2
                            #   parent arr, thread name, var name, mutex name
siccl_example_flattened = np.array([[0, 1, 2, 4],
                                    [0, 1, 3, 4],
                                    [1, 5, 2, 4], 
                                    [1, 5, 3, 0], 
                                    [5, 6, 2, 4], 
                                    [5, 6, 2, 4], 
                                    [5, 7, 2, 4]], dtype=int)
n_indices = len(siccl_example_flattened)
n_mutexe = 10
gamma = 0.99  # Discount factor for past rewards
max_steps_per_episode = 100



env = ConcurrencyDetectorEnvironment(siccl_example_flattened)
eps = np.finfo(np.float32).eps.item()  # Smallest number such that 1.0 + eps != 1.0

inputs = layers.Input(shape=(28,))
common = layers.Dense(num_hidden, activation="relu")(inputs)

action = layers.Dense(num_actions, activation="softmax")(common)
action_indices = layers.Dense(n_indices, activation="softmax")(common)
action_mutex_id = layers.Dense(n_mutexe, activation="softmax")(common)

critic = layers.Dense(1)(common)

model = keras.Model(inputs=inputs, outputs=[action, action_indices, action_mutex_id, critic])

"""
## Train
"""

optimizer = keras.optimizers.Adam(learning_rate=0.01)
huber_loss = keras.losses.Huber()
action_probs_history = []
critic_value_history = []
rewards_history = []
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

            action_probs, indices_probs, mutexe_probs, critic_value = model(state)
            critic_value_history.append(critic_value[0, 0])

            # Sample action from action probability distribution

            action = np.random.choice(a=num_actions, p=np.squeeze(action_probs))
            index = np.random.choice(a=n_indices, p=np.squeeze(indices_probs))
            mutex_id = np.random.choice(a=n_mutexe, p=np.squeeze(mutexe_probs))

            # adding average of multi action confidence to history
            action_probs_history.append(tf.math.log(np.average([action_probs[0, action], indices_probs[0, index], mutexe_probs[0, mutex_id]])))

            print(action, index, mutex_id)
            # Apply the sampled action in our environment
            state, reward, done = env.step((action, index, mutex_id))
            print(state)
            state = state.flatten()
            rewards_history.append(reward)
            episode_reward += reward

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
        for r in rewards_history[::-1]:
            discounted_sum = r + gamma * discounted_sum
            returns.insert(0, discounted_sum)

        # Normalize
        returns = np.array(returns)
        returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
        returns = returns.tolist()
        # Calculating loss values to update our network
        history = zip(action_probs_history, critic_value_history, returns)

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

        grads = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        # Clear the loss and reward history
        action_probs_history.clear()
        critic_value_history.clear()
        rewards_history.clear()

    # Log details
    episode_count += 1
    if episode_count % 10 == 0:
        template = "running reward: {:.2f} at episode {}"
        print(template.format(running_reward, episode_count))

    if running_reward > 195:  # Condition to consider the task solved
        print("Solved at episode {}!".format(episode_count))
        break
