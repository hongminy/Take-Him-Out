---
layout: default
title: Final Report
---

## Video:




<!-- blank line -->
<iframe align = "middle" width="672" height="378" src="https://www.youtube.com/embed/i7fdP1txuT0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<!-- blank line -->
  
## Project Summary
Our project is around a Minecraft fireball battle game that we developed. We configured the game ourselves following our own imaginations and using lots of ideas from other classic games like PONG and the mage battle from a map in Warcraft III.(Shown in Fig.1 and Fig.2) The reason why we choose to set up this environment is that we thought this is more like a real video game that we used to play daily and competitively, so this makes more sense to implement artificial intelligence on. 
<p>


</p> 
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/combined.png" alt="Warcraft III" width="953.4" height="315"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.1 Warcrat III maps that inspired our fireball game
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Pong.png" alt="Pong" width="640" height="300"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.2 The first two-player competitive video game
  </figcaption>
</figure>
<p>


</p>

To step up and make the environment more like a real video game, we restrict the actions our agent can take to some very general and non-trivial ones. The set of actions our agent can take consists of turning the head left and right (mouse movement), move forward and backward (W, S key), move left and right horizontally (A, S key) and throw the fireballs (mouse right-click). Given that all of our actions are continuous, I think they together make a perfect representation of how an actual human player would use mouse and keyboard to control the character, which sets our goal of the project to create an agent and learn how to play a game humanly, and would cause lots of challenges along the way. (Animated in Fig.3)
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Movement_demo.gif" alt="Movement demo" width="600" height="338"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.3 The set of movements allowed for our agent
  </figcaption>
</figure>
<p>


</p>
However, humans perceive the information from the game using their eyes, we decided to simplify our problem a little bit by inputting the numeric information directly to our agent instead of using another step of processing information from the images of the frames during the gameplay. This not only considerablely reduces our training time, since we wouldn't need to train a convolutional neural network to acquire data visually, but also making the implementation viable by avoiding working with the extremely distorting visual noise while throwing the fireballs. (Fig.4)
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/fireball.png" alt="Not good for conv net" width="929.7" height="279.9"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.4 When being thrown, the fireball completely covers up the screen
  </figcaption>
</figure>
<p>


</p>
The Final Training arena is a 10 x 10 square field with four walls with height 1 as its boarders.(Fig.5) After setting up the environment initially, there were lots of small changes that we had to make to the map, which turned out to be crutial along the way. For example, many changes were made in order to work with the fireballs. At first, the height of our walls are 4 blocks(both players are not able to see outside the arena). However if the agent releases the fireball too close to one of the walls, the speed of the fireball projectiles would be set to 0, resulting the fireballs not moving and be treated as the ones that Mincraft monsters released, which will damage the agent that throws those fireballs. To deal with that, we made the walls have only heights of 1, and the fireball would fly off the arena even if it's released close to a wall. 

We also reduced the size of the arena from its original size 20 x 20. After spending a few days training in a 20 x 20 map, we barely reached the 1000 episode mark. We realized that the high epsilon at the early stage, paring with a very large map would take us ages to train, since the agent rarely hit its target causing a long episode time. All above is the process of us coming up with the idea and setting up and finalizing the Minecraft environment that we used to train our agent.
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Arena.png" alt="Our simplfied arena" width="511.2" height="530"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.5 Our finallized arena
  </figcaption>
</figure>
<p>


</p>
## Approaches
Because we decided to have a continuous state space and action space, it would be implausible for us to use Tabular Q-Learning Reinforcement Learning to train our agent. The iterative process of computing and updating Q-values for each state-action pair in a large/continuous state space becomes computationally inefficient and perhaps infeasible due to the computational resources and time this may take. 
Instead, we chose to use Deep-Q Reinforcement Learning. With identical steps to tabular Q-learning, Deep-Q learning subsitude the part where the algorithm acquire Q-value from the Q-table to using neural networks to approximate a Q-value to the current state-action pair. Because Deep-Q learing doesn't have a actual Q-table stored in memory, Deep-Q learning is far less memory-consuming than Tabular Q-learning but might require more time to train. As the training progresses, the neural network should become better and better at approximating the Q-value by a given state-action pair(even continous ones).  
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Bellman.png" alt="Bellman Optimality Equation" width="594" height="205.8"/>
  <figcaption style="text-align:center; color:blue">
    Fig.6 Bellman Optimality Equation
  </figcaption>
</figure>
<p>


</p>
We read lots of blogs and articles about deep reinforcement learning and found out that the best way to implement this part is to use 2 neural networks: a policy net and a target net.  The policy net is to approximate the Q-value for the state-action pair from our original experience tuple and the target net is to approximate the target "optimal" Q-value from the same state-action pair. Then the difference between these 2 values is the loss of the policy network(Fig. 7). Since we are using the network to provide Q-value and use itself to evaluate, the target is moving all the time and it will cause the training extremely unstable(it's chasing its own tail all the time). Therefore, utilizing 2 different networks and only update the target net after several epochs can resolve this, hence the reason why we use 2 networks. 
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Bellman_2.png" alt="Policy net loss function" width="671.4" height="228.6"/>
  <figcaption style="text-align:center; color:blue">
    Fig.7 Policy network loss function
  </figcaption>
</figure>
<p>


</p>
The idea of "Replay Memory" is also introduced in our implementation, before the actual training starts, a replay memory of fixed size is initialized to store the agent's experiences at each time step in a data set. Each entry of the replay memory is represented as a tuple that contains the state, the action taken by the agent, the reward given to the agent at time t+1, and the next state of the environment, like a snippet of a Markov Transition. While training, the replay memory data is randomly sampled as the input of the policy network. If we just sequentially feed the input into the network, the samples would be highly correlated and would, therefore, lead to inefficient learning. Taking random samples from replay memory breaks this correlation. 

To Finallize our training setup, we used a python library called Keras RL that utilize tensorflow as background to make the 2 DQN networks. The type of our networks is Sequential(Basically a Multilayer Perceptron network), because we don't need to use any convolution or pooling layer to process images. The configuration of these 2 nets are identical, both having 2 layers of 256 perceptrons.

Curriculum learning is also used while training. At first our goal is to train the agent so that the agent can play against a moving target, so we set up the environment to let the agent play against a still, non-monving target. However, as we carried out the training, the agent didn't perform good enough to step up the difficulty, so we sticked to training and evaluating the performance against a still target. 

## Evaluation
Evaluation Plans: <br />
1) Compare the average scores and standard deviation between different setups<br />
2) Arrange an arena in which agents fight each other and count the win rate
<p>

               
</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Avg_score_excel.png" alt="Pong" width="997" height="132"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.1 The average scores against static opponent with different setups in different stages
  </figcaption>
</figure>
<p>


</p>
Interpretation of Fig.1: As we can see here the original setup with use coordinates of two agents as training state starts with a higher score in the beginning, but failed to reach scores higher than 163 and overfits quickly. Therefore we abandon  this setup after seeing scores drops under 160 and having the trend to drop further. It has higher standard deviation than other two non-random agents, that was caused by the high epislon = 0.3 fix. It performs more like a random agent than the other two. 

Setup No.2 has a better performance than No.1 because of the decaying epislon and better implementaion, using vector instead of coordinates as training state which helps the agent progress faster and reduce the size of state from 10 to 7. Decaying epislon also reduce the standard deviation. 

Setup No.3 has a larger learning rate of 0.01 instead of 0.005 as the previous two agents. The starting epislon was lower too. So it can get the higher scores in less episodes.
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Original_avg.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.2 Coordinate Setup avg score plot
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Original_score_dots.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.3 Coordinate Setup score dot plots
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/V_avg.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.4 Vector Setup No.1 avg score plot
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/V_score_dots.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.5 Vector Setup No.1 score dot plots
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/V_new_avg.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.6 Vector Setup No.2 avg score plot
  </figcaption>
</figure>
<p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/V_new_score_dots.png" alt="Pong" width="1036" height="355"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.7 Vector Setup No.2 score dot plots
  </figcaption>
</figure>
<p>


</p>
2) Agents fight against each other
 <p>


</p>
<figure style="text-align:center; margin-left: auto; margin-right: auto;">
  <img src="Pictures/Agents_against_each_other.png" alt="Pong" width="732" height="104"/>
  <figcaption style="text-align:center; color:blue">
  	Fig.8 Agents against each other
  </figcaption>
</figure>
<p>


</p>
<br />
<br />
The Vector Setup 1 has an overall better performance



## References

Reinforcement Learning - Introducing Goal Oriented Intelligence with deeplizard: <a href="https://deeplizard.com/learn/video/nyjbcRQ-uQ8">https://deeplizard.com/learn/video/nyjbcRQ-uQ8</a>

Deep Q Learning is Simple with Keras - Machine Learning with Phil: <a href="https://www.youtube.com/watch?v=5fHngyN8Qhw">https://www.youtube.com/watch?v=5fHngyN8Qhw</a>

Deep Reinforcement Learning for Keras: <a href="https://github.com/keras-rl/keras-rl">https://github.com/keras-rl/keras-rl</a>

Tensorflow GPU acceleration: <a href="https://www.tensorflow.org/guide/gpu">https://www.tensorflow.org/guide/gpu</a>

Nvidia CUDA installation: <a href="https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html">https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html</a>

Malmo Class references: <a href="http://microsoft.github.io/malmo/0.30.0/Documentation/index.html">http://microsoft.github.io/malmo/0.30.0/Documentation/index.html</a>

Malmo XML Schema Documentation: <a href="http://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html">http://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html</a>

Minecraft command references: <a href="https://minecraft.gamepedia.com/Commands">https://minecraft.gamepedia.com/Commands</a>

How to throw fireballs in Minecraft: <a href="https://www.youtube.com/watch?v=qYDetuX3cM8">https://www.youtube.com/watch?v=qYDetuX3cM8</a>
