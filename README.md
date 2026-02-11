# AMCOD: Acute Malignant Colorectal Obstruction Dataset

[**Paper**](LINK_TO_PAPER) | [**Dataset**](LINK_TO_DATASET) | [**BibTeX**](#citation)

**AMCOD** is the first NECT dataset specifically curated for the segmentation of colorectal obstruction in emergency scenarios. Unlike existing benchmarks that focus on elective surgery or normal anatomy, AMCOD addresses the critical domain shift caused by emergency pathology.

## 🔥 Why AMCOD?

Current segmentation models fail in emergency settings due to the **"Visual Gap"**:

1. **Modality Shift:** Routine datasets use Contrast-Enhanced CT (CECT), while emergencies rely on **Non-Contrast CT (NECT)**.
2. **Morphological Shift:** Normal intestines are tubular, while obstructed ones exhibit **Extreme Dilation** (proximal) and **Complete Collapse** (distal).

AMCOD provides **86 high-quality NECT scans** with voxel-level annotations to bridge this gap, serving as a robust benchmark for **Topological Continuity** and **Low-Contrast Segmentation**.

## 🚀 Dataset Highlights

- **Real-world Emergency Data:** Collected from a 10-year clinical cohort.
- **Pathological Topology:** Explicitly captures the transition from dilated to collapsed segments.
- **Challenging Benchmarks:** Targets the "Corner Cases" of medical segmentation (collapsed lumen, adhesions).



## 🧬 Dataset Construction Workflow

To ensure high-quality benchmarks, AMCOD follows a rigorous data curation pipeline, from cohort selection to final evaluation.

![Workflow](./figure/pic1.jpg)


Fig. 1 Overview of the AMCOD dataset construction workflow.

The pipeline consists of four key stages:

1. **Cohort Selection & Governance:** Strict inclusion/exclusion criteria with IRB approval and thorough de-identification.
2. **Preprocessing:** Standardization of orientation and metadata to ensure NIfTI compatibility.
3. **Consensus Annotation:** A "Human-in-the-loop" strategy where radiologists annotate functional segments (proximal, obstructed, distal), followed by expert verification.
4. **Evaluation:** Establishing baselines to benchmark segmentation performance.



## 👁️ Visualization of typical obstruction cases from the AMCOD 

AMCOD provides fine-grained, voxel-level annotations that explicitly capture the pathological topology of colorectal obstruction.

![Visualization](./figure/pic2.jpg)





**Legend:**

- 🟢 **Proximal Segment (Green):** Characterized by extreme **dilation** and fluid/gas accumulation.
- 🔴 **Obstructed Segment (Red):** The transition zone (tumor site), usually showing irregular wall thickening.
- 🔵 **Distal Segment (Blue):** Characterized by complete **collapse** and narrow lumen due to the obstruction.

As shown in the 3D reconstructions (d-f), the dataset captures the drastic morphological contrast between the dilated proximal colon and the collapsed distal colon, posing a significant challenge for topological consistency in segmentation models.

## 📜 Citation

Please cite our work if you use this dataset:

```bibtex

```
