# EEG Electrode Positions and Associated Brain Functions (32 Channels)

This document explains the standard positions of the 32 EEG electrodes used in this project, their corresponding cerebral cortex areas, and their primary functions. The naming and placement of these electrodes follow the internationally recognized **10-20 System**.

### Naming Convention

-   **Letter**: Represents a region (lobe) of the brain.
    -   **Fp**: Fronto-polar
    -   **F**: Frontal
    -   **C**: Central
    -   **T**: Temporal
    -   **P**: Parietal
    -   **O**: Occipital
-   **Number/Letter**: Indicates the position relative to the midline of the brain.
    -   **Odd Numbers**: Left Hemisphere
    -   **Even Numbers**: Right Hemisphere
    -   **'z'**: Midline

---

## Electrode Distribution and Functions by Brain Lobe

### 1. Frontal Lobe - Fp, F, FC

Electrodes in this area cover most of the forehead and are closely related to higher-order cognitive functions and motor control.

-   **Relevant Electrodes**: `Fp1`, `Fp2`, `F7`, `F3`, `Fz`, `F4`, `F8`, `FC5`, `FC1`, `FC2`, `FC6`
-   **Key Associated Functions**:
    -   **Motor Control**: Includes the **Primary Motor Cortex**, responsible for planning, controlling, and executing voluntary movements. **This is directly related to the `HandStart` and `LiftOff` events.**
    -   **Executive Functions**: Such as decision-making, problem-solving, planning, and attention.
    -   **Language**: Contains Broca's Area, which is primarily responsible for language production.
    -   **Emotion and Social Behavior**: Related to personality, impulse control, and social interaction.

### 2. Parietal Lobe & Central Area - P, C, CP

The parietal and central areas are core to processing sensory information and spatial awareness. The central area, straddling the frontal and parietal lobes, is home to the motor and sensory cortices.

-   **Relevant Electrodes**: `P7`, `P3`, `Pz`, `P4`, `P8`, `C3`, `Cz`, `C4`, `CP5`, `CP1`, `CP2`, `CP6`
-   **Key Associated Functions**:
    -   **Somatosensory Processing**: Includes the **Primary Somatosensory Cortex**, which processes sensations from the body like touch, temperature, pressure, and pain. **This is directly related to the tactile feedback from the `FirstDigitTouch` and `Replace` events.**
    -   **Spatial Awareness and Navigation**: Integrates sensory information to form an understanding of the surrounding environment.
    -   **Attention Allocation**.

### 3. Temporal Lobe - T, TP

The temporal lobe, located on the sides of the brain, is primarily responsible for hearing, memory, and language comprehension.

-   **Relevant Electrodes**: `T7`, `T8`, `TP9`, `TP10`
-   **Key Associated Functions**:
    -   **Auditory Processing**: Processes information about sound, including the pitch and volume of language.
    -   **Memory**: Home to the Hippocampus, which is crucial for the formation of long-term memories.
    -   **Language Comprehension**: Contains Wernicke's Area, responsible for understanding spoken and written language.

### 4. Occipital Lobe - O, PO

The occipital lobe, at the back of the brain, is the main visual processing center.

-   **Relevant Electrodes**: `O1`, `Oz`, `O2`, `PO9`, `PO10`
-   **Key Associated Functions**:
    -   **Visual Processing**: Receives and processes visual information from the eyes, including color, shape, and motion.
    -   **Object Recognition**.

---

## Summary Table

| Region | Channels | Key Associated Functions |
| :--- | :--- | :--- |
| **Frontal** | `Fp1`, `Fp2`, `F7`, `F3`, `Fz`, `F4`, `F8`, `FC1`, `FC2`, `FC5`, `FC6` | Motor planning and execution, decision-making, problem-solving, attention |
| **Central** | `C3`, `Cz`, `C4` | Primary Motor Cortex, Primary Somatosensory Cortex |
| **Parietal** | `P7`, `P3`, `Pz`, `P4`, `P8`, `CP1`, `CP2`, `CP5`, `CP6` | Somatosensation (touch, pressure), spatial awareness, sensory integration |
| **Temporal** | `T7`, `T8`, `TP9`, `TP10` | Audition, memory, language comprehension |
| **Occipital** | `O1`, `Oz`, `O2`, `PO9`, `PO10` | Visual processing |

## Relevance to the Grasp-and-Lift Project

-   **Motor Intention and Execution (`HandStart`, `LiftOff`)**: Primarily associated with activity in the **Frontal Lobe's** motor cortex and the **Central Area** (`C3`, `Cz`, `C4`).
-   **Tactile Feedback (`FirstDigitTouch`, `Replace`)**: Primarily associated with the **Parietal Lobe's** somatosensory cortex, as it processes tactile signals from the fingers.
-   **Visual Feedback**: While not a primary analysis target, the **Occipital Lobe** continuously processes visual information about the object's and hand's position during the task.
