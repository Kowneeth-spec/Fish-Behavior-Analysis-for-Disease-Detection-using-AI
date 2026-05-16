# Fish Behavior Analysis for Disease Detection using AI

> Non-invasive, real-time aquaculture disease detection through computer vision and deep learning

An AI-powered fish health monitoring system that analyzes underwater behavior patterns to detect disease outbreaks before visible symptoms appear — achieving 92%+ accuracy using Mask-RCNN segmentation, DeepSORT tracking, and a 5-parameter behavioral analysis engine.

Developed in collaboration with ZHAW University and Urbanblue AG, validated on rainbow trout in real aquaculture farms.

---

## Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Key Insight](#key-insight)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Behavioral Parameters](#behavioral-parameters)
- [Performance](#performance)
- [Impact](#impact)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Aquaculture disease outbreaks spread farm-wide within 24–48 hours. Traditional monitoring methods — manual observation, periodic blood tests — catch problems only after visible symptoms emerge, by which point mortality is already catastrophic.

This system continuously monitors fish behavior via underwater cameras. It detects subtle behavioral changes — reduced speed, erratic turning, surface-hugging — that precede physical symptoms by hours, enabling intervention when it still matters.

No animal handling. No invasive tests. No missed overnight events.

---

## The Problem

- Manual detection is too slow — disease spreads farm-wide in 24–48 hours while manual checks only catch problems after visible symptoms
- $10B+ in annual global losses from disease outbreaks causing mass mortality, costly treatments, and farm shutdowns
- Traditional methods fall short — blood tests are invasive and expensive; visual observation is inconsistent and only periodic

Early detection is the only viable solution.

---

## Key Insight

Sick fish behave differently BEFORE physical symptoms appear.

Speed drops. Schooling breaks down. Fish surface or sink. Turn angles become erratic. These behavioral signals are detectable hours before visible illness — and this system reads them automatically, around the clock.

---

## Features

- 24/7 automated monitoring with no human intervention required
- Real-time alerts in minutes, not hours or days
- 92%+ detection accuracy via deep learning
- Fully non-invasive — camera-only, zero animal handling
- Instance segmentation identifying and outlining each individual fish
- Multi-object tracking maintaining consistent fish identity across video frames
- 5-parameter behavioral analysis engine comparing live behavior to historical norms
- Correlation with expert observer ratings of 0.88–0.96 across all parameters

---

## System Architecture

The pipeline runs in three sequential stages:
