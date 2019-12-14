---
layout: default
title: Final Report
---

## Video:




<!-- blank line -->

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
Instead, we chose to use Deep-Q Reinforcement Learning:
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



## Evaluation
As a baseline, we expect our agent at least to perform rationally as a player in the arena we made, for example, attacking when the opponent is close, jumping to clear the obstacles and moving around normally. After an extended training and having a better designed Q-table, we want our agent to create a somewhat challenging combat environment for the other player. This involves the agent to be tactical, aggressive or conservative depends on its situation, good at using items, and well worn for combat. 


