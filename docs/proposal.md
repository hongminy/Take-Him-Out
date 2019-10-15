---
layout: default
title: Proposal
---
## Summary of the Proj
Minecraft-Cracker is a smart Minecraft combat agent that is designed to be optimized in our 1v1 Minecraft combat arena. The arena is designed to be competitive and tactical with obstacles, platforms and utility items. The rule is simple, at the end of the combat, the one player who still stands prevails. For our smart agent, a state might be a vector with multiple inputs like the location of the 2 players, the presence of certain items in the arena, the weapon they're using, etc. The trained policy function will then output a rational action to the state it is currently in. 

## AL/ML Algorithms
Standard Q-Learning with our manually observed features and tweaked Q-table

## Evaluation Plan
As a baseline, we expect our agent at least to perform rationally as a player in the arena we made, for example, attacking when the opponent is close, jumping to clear the obstacles and moving around normally. After an extended training and having a better designed Q-table, we want our agent to create a somewhat challenging combat environment for the other player. This involves the agent to be tactical, aggressive or conservative depends on its situation, good at using items, and well worn for combat. 
 