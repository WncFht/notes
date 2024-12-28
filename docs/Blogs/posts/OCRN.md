---
title: "Beyond Object Recognition: A New Benchmark towards Object Concept Learning"
tags:
  - 科研
categories: 
date: 2024-12-24T21:04:22+08:00
modify: 2024-12-24T21:04:22+08:00
dir: 
share: false
cdate: 2024-12-24
mdate: 2024-12-24
---

# Beyond Object Recognition: A New Benchmark towards Object Concept Learning

> [!info]+ 文章信息
> - 文章题目: Beyond Object Recognition: A New Benchmark towards Object Concept Learning
> - 作者：[Yong-Lu Li](https://arxiv.org/search/cs?searchtype=author&query=Li,+Y), [Yue Xu](https://arxiv.org/search/cs?searchtype=author&query=Xu,+Y), [Xinyu Xu](https://arxiv.org/search/cs?searchtype=author&query=Xu,+X), [Xiaohan Mao](https://arxiv.org/search/cs?searchtype=author&query=Mao,+X), [Yuan Yao](https://arxiv.org/search/cs?searchtype=author&query=Yao,+Y), [Siqi Liu](https://arxiv.org/search/cs?searchtype=author&query=Liu,+S), [Cewu Lu](https://arxiv.org/search/cs?searchtype=author&query=Lu,+C)
> - arXiv：[\[2212.02710\] Beyond Object Recognition: A New Benchmark towards Object Concept Learning](https://arxiv.org/abs/2212.02710)
> - 代码：[GitHub - silicx/ObjectConceptLearning: This the official repository of OCL (ICCV 2023).](https://github.com/silicx/ObjectConceptLearning)

> [!abstract]- Abstract
> Understanding objects is a central building block of AI, especially for embodied AI. Even though object recognition excels with deep learning, current machines struggle to learn higher-level knowledge, e.g., what attributes an object has, and what we can do with it. Here, we propose a challenging Object Concept Learning (OCL) task to push the envelope of object understanding. It requires machines to reason out affordances and simultaneously give the reason: what attributes make an object possess these affordances. To support OCL, we build a densely annotated knowledge base including extensive annotations for three levels of object concept (category, attribute, affordance), and the clear causal relations of three levels. By analyzing the causal structure of OCL, we present a baseline, Object Concept Reasoning Network (OCRN). It leverages concept instantiation and causal intervention to infer the three levels. In experiments, OCRN effectively infers the object knowledge while following the causalities well. Our data and code are available at https://mvig-rhos.com/ocl.

> [!note]- Conclusion
> In this work, we introduce object concept learning (OCL) expecting machines to infer affordances and explain what attributes enable an object to possess them. Accordingly, we build an extensive dataset and present OCRN based on casual intervention and instantiation. OCRN achieves decent performance and follows the causalities well. However, OCL remains challenging and would inspire a line of studies on reasoning-based object understanding.

## Model

- 通过 attribute 来预测 affordance，并推断是那些 attribute 起到了主要作用。

> [!example]-
> ![image.png](https://raw.githubusercontent.com/WncFht/picture/main/20241225134159699.png)

- 通过 casual intervetion 来避免 object category bias
- model implement 看的还是有点模糊，以后再来补充
