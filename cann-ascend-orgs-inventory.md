# CANN 与 Ascend 组织仓库清单（GitCode 主站实跑 + GitHub 镜像对照）

> 生成时间：2026-10-01（CST）｜ 数据来源：GitCode API v5 `GET /orgs/{cann|Ascend}/repos` 全量分页实跑；GitHub `GET /orgs/Ascend/repos` 实跑。
> 星标/更新时间均为 API 实测值，未手写。GitCode `/cann` 84 个、`/Ascend` 107 个；GitHub `Ascend` 组织 112 个（多为 GitCode 镜像）。

## 重要结论（先看这个）

- **CANN 的主站是 GitCode（`gitcode.com/cann`），不是 GitHub**。GitHub `Ascend/*` 里大量仓库描述写着 `Mirror of https://gitcode.com/...`（如 `pytorch`、`AscendNPU-IR`），即 GitHub 侧是镜像。
- **向 CANN 仓贡献需要先签 CLA**：`cann/ops-math` 的 CONTRIBUTING 原文——“完成 CLA 协议签署…签署 CLA”，流程指向 `gitcode.com/cann/community`；CI 门禁靠 **在 PR 下评论 `compile` 触发**，门禁通过后在关联 Issue 里 @ Committer。全流程中文。
- `Ascend/triton-ascend`（GitCode）描述已注明“已迁移到 https://github.com/triton-lang/triton-ascend” ⇒ 我们的 triton-ascend PR 方向是对的。

## 一、GitCode /cann（84 个：CANN 计算架构本体）

| 分类 | 仓数 | 代表仓（按星标） |
|---|---|---|
| 算子库 / 算子工程（ops-*） | 16 | `ops-math`(1473★)、`ops-transformer`(1323★)、`ops-nn`(1039★)、`ops-cv`(656★) |
| 社区治理 / 基建 / 评测 / Bot | 13 | `cannbot-skills`(1949★)、`infrastructure`(326★)、`cann-outreach`(268★)、`release-management`(260★) |
| 其它 / 新近仓 | 12 | `pypto`(1086★)、`torchtitan-npu`(566★)、`ascend-transformer-boost`(426★)、`asnumpy`(406★) |
| 学习 / 样例 / 竞赛（recipes-*） | 10 | `cann-learning-hub`(1378★)、`cann-recipes-infer`(983★)、`cann-samples`(742★)、`cann-recipes-train`(614★) |
| 行业 SIG（电力/交通/油气/化工/密码） | 9 | `mat-chem-sim-pred`(162★)、`elec-ops-prediction`(145★)、`elec-ops-inspection`(144★)、`elec-ops-simulation`(138★) |
| Ascend C 语言、模板与算子开发工具 | 8 | `asc-devkit`(925★)、`catlass`(619★)、`pto-isa`(452★)、`pyasc`(409★) |
| 通信 / 集合通信 | 8 | `hixl`(886★)、`community`(868★)、`hccl`(559★)、`hcomm`(508★) |
| 图引擎 / 运行时 / 驱动 / 基础框架 | 7 | `ge`(782★)、`opbase`(734★)、`graph-autofusion`(721★)、`runtime`(671★) |
| 模型压缩 / 量化 | 1 | `amct`(410★) |

### 算子库 / 算子工程（ops-*）（16）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `ops-math` | 1473 | 1519 | 2025-09-25 | 本项目是CANN提供的数学类基础计算算子库，实现网络在NPU上加速计算。 |
| `ops-transformer` | 1323 | 3014 | 2025-09-28 | 本项目是CANN提供的transformer类大模型算子库，实现网络在NPU上加速计算。 |
| `ops-nn` | 1039 | 1937 | 2025-09-27 | 本项目是CANN提供的神经网络类计算算子库，实现网络在NPU上加速计算。 |
| `ops-cv` | 656 | 431 | 2025-09-26 | 本项目是CANN提供的图像处理、目标检测相关的算子库，实现网络在NPU上加速计算。 |
| `ops-blas` | 234 | 380 | 2026-03-31 | 本项目是CANN提供的高性能线性代数计算以及轻量化GEMM调用算子库。 |
| `ops-test-kit` | 232 | 201 | 2026-05-12 | TTK（Ops Test Tool Kit）是CANN算子库提供的全链路、自动化、批量化算子测试框架，帮助开发者快速完成算子批量功能验证、性能评估以及Golden值比对，提升算子开 |
| `ops-tensor` | 220 | 149 | 2026-04-16 | ops-tensor 是 CANN （Compute Architecture for Neural Networks）算子库中提供张量类计算的基础算子库，采用模块化设计，支持灵活 |
| `ops-sparse` | 204 | 239 | 2026-04-30 | 本项目是CANN提供的高性能稀疏矩阵计算的算子库，专注于优化稀疏矩阵的计算效率。 |
| `ops-solver` | 161 | 49 | 2026-04-30 | 本项目是CANN提供的高级数值求解算子库，实现矩阵分解、求逆、特征值求解等功能在NPU上的加速计算。 |
| `ops-fft` | 151 | 30 | 2026-04-16 | ops-fft 是 CANN （Compute Architecture for Neural Networks）算子库中提供 FFT 类计算的基础算子库，采用模块化设计，支持灵活 |
| `ops-collections` | 149 | 62 | 2026-04-20 | ops-collections是基于昇腾硬件的高性能容器模板库，提供运行在NPU上的static_map、dynamic_map、set等容器。利用最新的SIMT并发能力，支持对容 |
| `ops-rand` | 139 | 14 | 2026-04-16 | ops-rand是CANN （Compute Architecture for Neural Networks）算子库中提供的随机数生成库。 |
| `ops-multimodal-fusion` | 138 | 20 | 2026-06-17 | 基于 AscendC 的 PyTorch 自定义多模态算子库 |
| `ops-gnn` | 121 | 65 | 2026-07-22 | ops-gnn是昇腾生态下图神经网络（GNN）算子和特性的集合， 支持PYG和DGL框架。 |
| `ops-ras` | 107 | 36 | 2026-08-12 |  |
| `ops-tilelang` | 32 | 5 | 2026-09-30 | ops-tilelang 是 CANN 社区面向昇腾 NPU 的 TileLang 高性能算子仓，旨在通过统一管理 Kernel 实现、自动化测试用例、标准工作负载和性能基线，为开 |

### 社区治理 / 基建 / 评测 / Bot（13）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `cannbot-skills` | 1949 | 1165 | 2026-04-30 | CANNBot 是面向 CANN 开发的用于提升开发效率的系列智能体，本仓库为其提供可复用的 Skills 模块。 |
| `infrastructure` | 326 | 70 | 2026-06-08 | 本仓库用于托管CANN社区基础设施团队的公开信息，包括不限于：会议日程，成员信息，服务文档和配置等信息 |
| `cann-outreach` | 268 | 2366 | 2026-05-15 |  |
| `release-management` | 260 | 91 | 2026-01-04 | CANN版本发布管理仓库 |
| `cann-bench` | 234 | 140 | 2026-04-30 | 评测AI在处理CANN领域代码任务的能力，涵盖算子生成、算子优化等领域，支撑模型选型、训练效果评估，统一量化评估标准，识别Agent能力短板，构建CANN领域评测平台，推动AI能力 |
| `cann-agreements` | 151 | 0 | 2026-04-20 | CANN 迁移协议签署 |
| `.gitcode` | 140 | 32 | 2026-04-24 | CANN组织的模板文件 |
| `docs` | 135 | 39 | 2026-07-03 | 该仓库用于维护cann公共文档 |
| `cann-spack-package` | 134 | 14 | 2026-03-27 | 本项目用于管理CANN社区Spack包管理package.py配置文件，Spack包管理器通过解析这些文件，可动态地将用户指定的软件规格（Spec）转化为实际的构建、安装、部署命令 |
| `manifest` | 132 | 8 | 2026-03-12 | 本项目是 CANN 的 manifest 配置仓库，用于通过 repo 工具管理和同步 CANN 相关的多个代码仓，定义 CANN 组件的仓库地址、分支版本和目录结构 |
| `cannbot` | 100 | 43 | 2026-09-02 | CANNBot 是面向 CANN 开发的用于提升开发效率的系列智能体，本仓库为其提供plugin、harness等应用模块。 |
| `cannbot-sentry` | 77 | 22 | 2026-09-10 | CANN 生态中面向 Agent 工作流的“哨兵”：观测 · 审计 · 评测三位一体的质量基础设施 |
| `cannbot-knowledge` | 74 | 32 | 2026-09-15 | cannbot算子开发知识库插件依赖的知识库本体仓，给cannbot提供统一的知识底座。 |

### 其它 / 新近仓（12）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `pypto` | 1086 | 736 | 2026-04-13 | PyPTO（发音: pai p-t-o）：Parallel Tensor/Tile Operation编程范式。 |
| `torchtitan-npu` | 566 | 186 | 2026-04-16 | Ascend Extension for torchtitan |
| `ascend-transformer-boost` | 426 | 168 | 2025-11-18 | 本项目是CANN提供的是一款高效、可靠的Transformer加速库，基于华为Ascend AI处理器，提供Transformer定制化场景的高性能融合算子。 |
| `asnumpy` | 406 | 61 | 2026-08-28 | 哈尔滨工业大学计算学部苏统华、王甜甜老师团队联合华为CANN团队开发的华为昇腾NPU原生Numpy仓库 |
| `oam-tools` | 390 | 170 | 2026-09-30 | 本项目为开发者提供故障定位工具，包含故障信息收集，软硬件信息展示，AI core error报错分析等能力，提升故障问题定位效率，文档可在昇腾社区搜索“故障处理简介”（选择社区版） |
| `sip` | 336 | 75 | 2025-11-05 | 本项目是CANN提供的一款高效、可靠的高性能信号处理算子加速库，基于华为Ascend AI处理器，专门为信号处理领域而设计。 |
| `triton-inference-server-ge-backend` | 332 | 19 | 2025-12-12 | ge-backend基于triton inference server框架实现对接NPU生态，快速实现传统CV\NLP等模型的服务化。 |
| `tensorflow` | 166 | 34 | 2026-04-10 | Ascend TensorFlow Adapter |
| `xla-npu` | 154 | 14 | 2026-04-17 | XLA-NPU 是一个面向华为昇腾NPU硬件的 XLA后端实现。本项目通过接入OpenXLA/XLA开源项目，将XLA开源生态与华为 CANN软件栈集成，对接JAX框架。JAX框架 |
| `asnumpy-docs` | 142 | 12 | 2026-05-13 |  |
| `gauss-splat` | 126 | 13 | 2026-07-30 | 本项目是基于CANN的3D Gaussian Splatting渲染加速库，通过Ascend C算子加速核心计算，提供高性能的PyTorch扩展接口，覆盖3DGS训练和推理全流程。 |
| `npu-simulator` | 13 | 4 | 2026-09-30 | NPUSim（全称NPU Simulator）是一款面向算子开发场景的SoC级芯片仿真工具，用于分析运行在AI仿真器上的AI任务在各阶段的精度和性能数据（如指令执行情况等）。该工具 |

### 学习 / 样例 / 竞赛（recipes-*）（10）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `cann-learning-hub` | 1378 | 606 | 2026-04-27 | CANN 学习中心仓，支持在线互动运行、边学边练，提供教程、示例与优化方案，一站式助力昇腾开发者快速上手。 |
| `cann-recipes-infer` | 983 | 576 | 2025-09-29 | 本项目针对LLM与多模态模型推理业务中的典型模型、加速算法，提供基于CANN平台的优化样例 |
| `cann-samples` | 742 | 226 | 2026-09-01 | CANN高性能实战演进样例与体系化调优知识库 |
| `cann-recipes-train` | 614 | 115 | 2025-10-29 | 本项目针对LLM与多模态模型训练业务中的典型模型、加速算法，提供基于CANN平台的优化样例 |
| `cann-recipes-embodied-ai` | 385 | 73 | 2026-05-19 | 本项目针对具身智能业务中的典型模型、加速算法，提供基于CANN平台的优化样例 |
| `pypto-gym` | 334 | 231 | 2026-06-26 | PyPTO-Gym 是基于 PyPTO 编程框架构建的算子与模型样例仓库 |
| `cann-ops-competitions` | 319 | 1123 | 2026-05-27 | 本仓库用于 CANN 开源社区各类竞赛、开源课题、社区任务等课题发布、开发者作品提交和展示。 |
| `cann-recipes-harmony-infer` | 315 | 51 | 2025-12-26 | 本项目为鸿蒙开发者提供基于CANN平台的业务实践案例，方便开发者参考实现端云能力迁移及端侧推理部署。 |
| `cann-recipes-spatial-intelligence` | 306 | 24 | 2025-12-02 | 本项目针对空间智能业务中的典型模型、加速算法，提供基于CANN平台的优化样例 |
| `cann-launch-camp` | 190 | 712 | 2026-06-16 | 用户可借助此项目规范管理 CANN 开源社区启航营高校活动的课程作业、课设、毕设等实践作品，其核心功能是统一标准化目录层级与提交规范，保障作品提交规整、可追溯、可评审。 |

### 行业 SIG（电力/交通/油气/化工/密码）（9）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `mat-chem-sim-pred` | 162 | 13 | 2026-02-10 | 面向工业领域，聚焦计算仿真、预测两大核心场景，构建面向流程工业"机理+数据"双轮驱动的领域计算层，推动AI for Science在材料化学领域的深度应用。 |
| `elec-ops-prediction` | 145 | 8 | 2026-03-14 | elec-ops-prediction 是 CANN 社区 Electrical Engineering SIG（电力行业兴趣小组）旗下的电力负荷预测算子库， 聚焦于电力系统运行、 |
| `elec-ops-inspection` | 144 | 34 | 2026-03-14 | elec-ops-inspection 是 CANN 社区 Electrical Engineering SIG（电力行业兴趣小组）旗下的电力装备巡检算子库， 覆盖 CV 视觉检测 |
| `elec-ops-simulation` | 138 | 7 | 2026-03-16 | elec-ops-simulation 是 CANN 社区 Electrical Engineering SIG（电力行业兴趣小组）旗下的电力仿真求解算子库， 聚焦于计算电网在稳态 |
| `its-matrix-computation` | 103 | 6 | 2026-08-06 | its-matrix-computation 是 transportation SIG 下的矩阵计算优化仓库，面向昇腾平台 GEMM 分块策略自动优化场景，聚焦大模型训练与推理中的 |
| `its-stable-llm` | 102 | 6 | 2026-08-06 | its-stable-llm 是 transportation SIG 下的大模型训练稳定性分析仓库，面向大模型训练过程中的稳定性监控、微批次分布建模和失稳前兆识别。仓库将把 st |
| `its-trip` | 102 | 8 | 2026-08-06 | its-trip 是 transportation SIG 下的交通大模型智能决策闭环仓库，面向交通事件处置、交通管控决策和交通智能体应用场景，构建“感知—研判—仿真—下发”的闭环 |
| `crypto` | 62 | 15 | 2026-09-16 | crypto SIG 是密码学兴趣小组，围绕昇腾 NPU 打造高性能密码软件库，提供丰富的密码算子与算法实现 |
| `oil-gas-ops-prospect` | 54 | 13 | 2026-09-16 | 面向油气勘探（oil & gas exploration）领域的昇腾自定义算子库。仓名即 oil-gas-ops（油气算子）+ prospect（勘探目标），面向地震成像、全波形反 |

### Ascend C 语言、模板与算子开发工具（8）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `asc-devkit` | 925 | 1122 | 2026-06-06 | 本项目是CANN 推出的昇腾AI处理器专用的算子程序开发语言，原生支持C和C++标准规范，主要由类库和语言扩展层构成，提供多层级API，满足多维场景算子开发诉求。 |
| `catlass` | 619 | 319 | 2025-10-27 | 本项目是CANN的算子模板库，提供NPU上高性能矩阵乘及其相关融合类算子模板样例。 |
| `pto-isa` | 452 | 286 | 2025-12-27 | Parallel Tile Operation (PTO) is a virtual instruction set architecture designed by Ascend |
| `pyasc` | 409 | 69 | 2025-11-28 | 本项目为Python用户提供算子编程接口，支持在昇腾AI处理器上加速计算，接口与Ascend C一一对应并遵守Python原生语法。 |
| `atvoss` | 385 | 45 | 2025-11-29 | ATVOSS（Ascend C Templates for Vector Operator Subroutines）是一套基于Ascend C开发的Vector算子库，致力于为昇腾 |
| `asc-tools` | 339 | 167 | 2025-11-29 | Ascend C Tools仓是CANN基于Ascend C编程语言推出的配套调试工具仓。 |
| `atvc` | 298 | 23 | 2025-11-15 | ATVC（Ascend C Templates for Vector Compute），是为基于Ascend C开发的典型Vector算子封装的一系列模板头文件的集合，可帮助用户快 |
| `cannbot-dsl` | 176 | 81 | 2026-08-05 | 基于 CANNBot-DSL 的 Ascend NPU 复杂算子示例集合。 |

### 通信 / 集合通信（8）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `hixl` | 886 | 154 | 2025-10-15 | HIXL（Huawei Xfer Library）是一个灵活、高效的昇腾单边通信库，面向集群场景提供简单、可靠、高效的点对点数据传输能力。 |
| `community` | 868 | 476 | 2025-09-25 | 本项目是CANN开源社区的核心管理仓库，包含社区的治理章程、治理组织、通用操作指引及流程规范等基础信息 |
| `hccl` | 559 | 669 | 2025-12-01 | 集合通信库（Huawei Collective Communication Library，简称HCCL）是基于昇腾AI处理器的高性能集合通信库，为计算集群提供高性能、高可靠的通信 |
| `hcomm` | 508 | 1017 | 2025-12-01 | HCOMM（Huawei Communication）是HCCL的通信基础库，提供通信域以及通信资源的管理能力。 |
| `ascend-boost-comm` | 305 | 39 | 2025-09-30 | 算子公共平台，南向对接不同组织开发的算子库，北向支撑不同加速库应用，实现M x N算子能力复用 |
| `shmem` | 295 | 198 | 2025-12-30 | CANN SHMEM 是面向昇腾平台的多机多卡内存通信库，基于OpenSHMEM 标准协议，实现跨设备的高效内存访问与数据同步。 |
| `catccos` | 171 | 50 | 2026-04-20 | CATCCOS昇腾计算-通信融合算子模板库，是一个聚焦于提供高性能计算通信融合类算子基础模板的代码库。 |
| `asc-comm` | 128 | 80 | 2026-07-30 | 本项目是CANN 推出的昇腾AI处理器面向通算融合场景打造的专属开源仓库，屏蔽硬件差异，为底层硬件协同与上层通信算法落地提供统一&高性能数据面。 |

### 图引擎 / 运行时 / 驱动 / 基础框架（7）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `ge` | 782 | 511 | 2026-09-09 | GE（Graph Engine）是面向昇腾的图编译器和执行器，提供了计算图优化、多流并行、内存复用和模型下沉等技术手段，加速模型执行效率，减少模型内存占用。 GE 提供对 PyTo |
| `opbase` | 734 | 251 | 2025-09-25 | 本项目是CANN算子库的基础框架库，为算子提供公共依赖文件和基础调度能力。 |
| `graph-autofusion` | 721 | 271 | 2026-08-03 | Graph-autofusion 是一个面向昇腾（Ascend）芯片的轻量级、解耦式组件集合，旨在通过自动融合技术加速模型执行。 目前已开源 SuperKernel 组件和 Aut |
| `runtime` | 671 | 820 | 2025-12-25 | 本项目提供CANN运行时组件和维测功能组件。 |
| `metadef` | 534 | 128 | 2025-12-26 | Ascend Metadata Definition |
| `driver` | 382 | 150 | 2025-12-24 | 本项目是CANN提供的驱动模块，实现基础驱动和资源管理及调度等功能，使能昇腾芯片。 |
| `cmake` | 168 | 59 | 2026-04-09 | 本项目提供公共编译脚本、第三方开源软件编译脚本、公共打包与安装框架脚本 |

### 模型压缩 / 量化（1）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `amct` | 410 | 116 | 2025-12-22 | AMCT是CANN提供的昇腾AI处理器亲和的模型压缩工具仓。 |

## 二、GitCode /Ascend（107 个：昇腾生态与工具链）

| 分类 | 仓数 | 代表仓（按星标） |
|---|---|---|
| MindStudio 工具链（ms* 调试/调优/分析） | 30 | `msmodelslim`(332★)、`msinsight`(286★)、`msprobe`(216★)、`msit`(180★) |
| 其它 | 26 | `AscendNPU-IR`(981★)、`RecSDK`(135★)、`AgentSDK`(88★)、`DrivingSDK`(86★) |
| PyTorch 生态适配（torch_npu / 图模式 / 插件） | 13 | `torchair`(916★)、`pytorch`(890★)、`op-plugin`(189★)、`fbgemm-ascend`(20★) |
| 训练加速（MindSpeed / Megatron / TE / FSDP） | 8 | `MindSpeed-LLM`(215★)、`MindSpeed-MM`(176★)、`MindSpeed`(88★)、`MindSpeed-RL`(74★) |
| 社区治理 / 生态 / Agent | 7 | `agent-skills`(191★)、`slime-ascend`(26★)、`docs`(13★)、`ascend-agreements`(12★) |
| 集群 / ModelZoo / CI 基建 | 7 | `mind-cluster`(199★)、`ModelZoo-PyTorch`(83★)、`mindcluster-deploy`(82★)、`modelzoo-GPL`(15★) |
| 推理引擎与服务化（MindIE） | 6 | `MindIE-LLM`(137★)、`MindIE-SD`(119★)、`MindInferenceService`(55★)、`MindIE-Motor`(54★) |
| 编译器 / IR / Triton | 5 | `triton-ascend`(189★)、`triton-ascend-kernels`(29★)、`ascendc-kernelgen-data`(22★)、`llvm-project`(3★) |
| 通信 / 内存池化 | 3 | `memfabric_hybrid`(178★)、`memcache`(154★)、`community`(33★) |
| 行业 / 领域 SDK | 2 | `faiss`(16★)、`text-embeddings-inference`(5★) |

### MindStudio 工具链（ms* 调试/调优/分析）（30）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `msmodelslim` | 332 | 204 | 2025-12-30 | MindStudio-ModelSlim（msModelSlim）是MindStudio全流程工具链推出的模型量化压缩工具。 |
| `msinsight` | 286 | 84 | 2026-03-16 | 针对大模型训练&&推理场景，提供可视化调优能力，辅助用户更快定位模型性能问题 |
| `msprobe` | 216 | 148 | 2025-12-30 | 针对昇腾提供的全场景精度工具链，帮助用户快速提高模型精度定位效率。 |
| `msit` | 180 | 191 | 2025-09-07 | 统一推理工具链入口，提供客户一体化开发工具，支持一站式调试调优。 |
| `msprof` | 138 | 57 | 2026-01-04 | MindStudio Profiler（msProf，模型调优工具）提供了AI任务运行性能数据、昇腾AI处理器系统数据等性能数据的采集和解析功能，这些功能侧重不同的训练或推理场景， |
| `mstt` | 138 | 127 | 2025-09-07 | 针对训练&大模型场景，提供端到端命令行&可视化调试调优工具，帮助用户快速提高模型开发效率。 |
| `model-agent` | 125 | 155 | 2026-04-10 | 昇腾模型 Agent，大模型落地全流程一键通！查适配、做调优、快部署、稳上线，文档一键生成，一站式搞定无压力！ |
| `msagent` | 123 | 146 | 2026-04-07 | MindStudio智能体，提供性能和精度等自动分析功能 |
| `msprof-analyze` | 118 | 57 | 2025-12-30 | MindStudio-Profiler-Analyze（msprof-analyze）是MindStudio全流程工具链推出的性能分析工具，基于采集的性能数据进行分析，识别AI作业 |
| `msopprof` | 116 | 52 | 2025-12-30 | NA |
| `msmemscope` | 112 | 29 | 2025-12-30 | MindStudio-MemScope（msmemscope）是MindStudio推出的整网内存调试调优工具，提供内存数据采集、辅助分析、自动诊断等能力。 |
| `msot` | 109 | 35 | 2025-12-30 | NA |
| `ascend-deployer` | 108 | 103 | 2025-12-31 | 昇腾软件安装部署参考设计，提供系统组件、python第三方依赖自动下载以及一键式安装的功能，并支持驱动、固件、CANN软件包以及MindCluster的安装。 |
| `mindsdk-referenceapps` | 108 | 61 | 2025-09-07 | MindSDK Reference Apps |
| `mssanitizer` | 105 | 50 | 2025-12-30 | NA |
| `msserviceprofiler` | 105 | 84 | 2025-12-30 | MindStudio-Service-Profiler（msserviceprofiler）是MindStudio推理服务化性能数据采集工具，采集关键过程的开始和结束时间点，识别关 |
| `msmonitor` | 105 | 25 | 2025-12-30 | MindStudio-Monitor（msmonitor）是MindStudio全流程工具链推出的一站式在线监控工具，提供用户在集群场景性能监控定位端到端能力。 |
| `mspti` | 101 | 40 | 2026-01-08 | msPTI工具（MindStudio Profiling Tools Interface）是MindStudio针对Ascend设备提出的一套Profiling API，用户可以通 |
| `msdebug` | 99 | 36 | 2025-12-30 | NA |
| `msmodeling` | 93 | 207 | 2026-06-23 | MindStudio-Modeling（msmodeling）是MindStudio建模寻优工具，评估模型及服务化等场景下的理论性能，并在此基础上寻找性能较优的部署策略等参数。 |
| `msopcom` | 90 | 35 | 2025-12-30 | NA |
| `msopgen` | 89 | 25 | 2025-12-30 | NA |
| `mstx` | 86 | 26 | 2025-12-30 | NA |
| `mskpp` | 84 | 22 | 2025-12-30 | NA |
| `msoptuner` | 82 | 18 | 2025-12-30 | NA |
| `mskl` | 82 | 19 | 2025-12-30 | NA |
| `ascend-docker-image` | 61 | 19 | 2025-09-07 | 提供Ascend相关的Dockerfile示例，展示如何创建docker镜像。 |
| `solution-agent` | 23 | 2 | 2026-09-01 | solution-agent 仓库是昇腾（Ascend）社区用于辅助开发者快速开发和部署行业场景解决方案的平台，提供方案参考设计、环境快速部署、性能优化等能力，助力各行业快速构建行 |
| `mscommreport` | 9 | 4 | 2026-03-13 | 提供HCCL中断类问题自动分析能力，帮助开发及维护人员提升HCCL问题分析效率 |
| `msboost` | 7 | 24 | 2026-06-02 | 针对AI推理训练场景构建极致性能加速工具。 |

### 其它（26）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `AscendNPU-IR` | 981 | 432 | 2026-03-06 | AscendNPU-IR是基于MLIR（Multi-Level Intermediate Representation）构建的，面向昇腾亲和算子编译时使用的中间表示，提供昇腾完备表 |
| `RecSDK` | 135 | 208 | 2025-09-07 | 华为昇腾-MindX 推荐SDK |
| `AgentSDK` | 88 | 79 | 2025-12-29 | AgentSDK |
| `DrivingSDK` | 86 | 179 | 2025-09-13 | 华为昇腾-自动驾驶加速库 |
| `IndexSDK` | 81 | 90 | 2026-04-24 | 基于华为昇腾平台Index SDK实现了一个高效的向量特征检索引擎，用户可以在此引擎上实现面向应用场景的检索系统 |
| `VisionSDK` | 75 | 56 | 2025-12-31 | 面向图片和视频视觉分析的SDK，提供了基本的视频、图像智能分析能力及编程框架 |
| `RAGSDK` | 73 | 59 | 2025-12-29 | RAG SDK是昇腾面向大语言模型的知识增强开发套件，为解决大模型知识更新缓慢以及垂直领域知识回答弱的问题，面向大模型知识库提供垂域调优、生成增强、知识管理等特性，帮助用户搭建专属 |
| `MultimodalSDK` | 64 | 49 | 2025-12-30 | MultimodalSDK |
| `MEF` | 55 | 36 | 2025-12-30 | 使能构建边云协同平台、管理边缘AI业务，提供安全、可信、完整的轻量化端边云框架 |
| `OMSDK` | 53 | 32 | 2025-12-30 | 使能构建边云协同平台、管理边缘AI业务，提供安全、可信、完整的轻量化端边云框架 |
| `Triton-distributed-ascend` | 21 | 67 | 2026-09-16 | Triton-distributed-ascend 是基于 Triton 语言扩展的分布式计算框架，专门为昇腾（Ascend）AI处理器优化。该项目提供了在昇腾NPU上进行高效分布 |
| `ATK` | 18 | 29 | 2026-05-19 | NA |
| `HierarchicalKV-ascend` | 17 | 27 | 2026-04-14 | 基于昇腾平台，面向推荐系统的高性能key-value存储加速库 |
| `TransferQueue` | 15 | 9 | 2026-01-04 | 异步高性能流式数据引擎 |
| `FSDPTurbo` | 11 | 63 | 2026-06-30 | 提供NPU亲和的FSDP增强特性 |
| `TransformerEngineNPU` | 8 | 46 | 2026-05-21 | 提供适配昇腾的TransformerEngine加速库 |
| `EcoDevHub` | 7 | 315 | 2026-09-07 | EcoDevHub 仓库是昇腾（Ascend）社区用于支持生态发展的仓库，通过本仓库集中沉淀生态技术创新项目、外部案例、竞赛成果、社区任务等。 |
| `DeepEP` | 6 | 22 | 2026-09-16 | DeepEP底层高性能通信库的昇腾版本 |
| `MindCluster-AscendNPUBurn` | 6 | 23 | 2026-05-25 | 面向昇腾芯片/链路硬件，提供故障压测算子、模型用例 |
| `mockcpp` | 6 | 4 | 2025-12-30 | mockcpp是一个轻量级的C++单元测试框架。此fork用于支持MindStudio等项目。 |
| `MegatronAdaptor` | 4 | 28 | 2026-05-21 | 提供Megatron-LM在昇腾上的基础适配 |
| `MoonEP` | 3 | 2 | 2026-09-08 | MoonEP负载均衡能力的昇腾版本 |
| `ray-ascend` | 3 | 5 | 2026-02-01 | Ascend-native hardware plugin for ray |
| `Tensorpipe` | 3 | 11 | 2025-09-13 |  |
| `FlashGen` | 2 | 15 | 2026-08-25 | MindIE FlashGen 是一个面向多模态生成的以训助推(Training-aware Acceleration)加速套件。通过深度融合步数蒸馏、量化感知训练与可学习稀疏注意 |
| `TorchTitanTurbo` | 0 | 5 | 2026-07-23 | 提供亲和昇腾NPU的Torch实验性加速特性 |

### PyTorch 生态适配（torch_npu / 图模式 / 插件）（13）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `torchair` | 916 | 429 | 2025-11-03 | TorchAir 支持用户基于PyTorch框架和torch_npu插件在昇腾NPU上使用图模式进行推理。 |
| `pytorch` | 890 | 1409 | 2026-07-20 | 作为 Ascend for PyTorch 社区的核心组件，TorchNPU 是昇腾专为 PyTorch 打造的深度学习适配插件，使 PyTorch 框架能够直接调用昇腾 NPU， |
| `op-plugin` | 189 | 884 | 2026-07-31 | OpPlugin of Ascend for PyTorch |
| `fbgemm-ascend` | 20 | 53 | 2026-06-29 | 基于昇腾平台，重点关注推荐系统的高性能PyTorch NPU算子库 |
| `vision` | 12 | 14 | 2025-12-29 | 本项目开发了Torchvision Adapter插件，用于昇腾适配Torchvision框架。 目前该适配框架增加了对Torchvision所提供的常用算子的支持，提供了基于cv |
| `apex` | 11 | 9 | 2025-09-13 | Ascend apex adapter |
| `pytorch-ecosystem` | 9 | 48 | 2026-08-03 | The official repository of Ascend for PyTorch ecological activities. |
| `ops-rec` | 8 | 24 | 2026-06-23 | 基于昇腾平台，面向推荐系统的高性能融合算子仓库 |
| `torchao_npu` | 2 | 18 | 2026-08-31 | Ascend Extension for PyTorchAO |
| `torchcomms_npu` | 2 | 6 | 2026-08-10 | The official repository of Ascend for PyTorch ecological activities. |
| `torch-mlir` | 2 | 0 | 2025-11-25 | torch-mlir 旨在为 MLIR 生态系统提供来自 PyTorch 生态系统的支持。此fork用于添加昇腾上编译器的功能，支持AscendNPU IR等 |
| `taco` | 1 | 1 | 2026-08-13 | Torch Ascend Custom Operators |
| `monarch_npu` | 0 | 0 | 2026-09-01 | The official repository of Ascend for PyTorch ecological activities. |

### 训练加速（MindSpeed / Megatron / TE / FSDP）（8）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `MindSpeed-LLM` | 215 | 335 | 2025-11-03 | 昇腾LLM分布式训练框架 |
| `MindSpeed-MM` | 176 | 383 | 2025-12-25 | 华为昇腾面向大规模分布式训练的多模态大模型套件，支撑多模态生成、多模态理解。 |
| `MindSpeed` | 88 | 397 | 2025-09-13 | 昇腾大模型加速库 |
| `MindSpeed-RL` | 74 | 137 | 2025-09-13 | 昇腾强化学习加速库 |
| `MindSpeed-Ops` | 14 | 73 | 2026-04-07 | 提供昇腾优化的训练业务自定义算子实现 |
| `MindSpeed-Bridge` | 13 | 45 | 2026-04-07 | 提供昇腾适配的更多Bridge模型代码 |
| `MindSpeed-Agent` | 9 | 38 | 2026-07-06 | 提供MindSpeed系列套件开发agent |
| `MindSpeed-Core-MS` | 8 | 20 | 2026-01-15 | MindSpore动态图大模型加速库 |

### 社区治理 / 生态 / Agent（7）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `agent-skills` | 191 | 157 | 2026-02-26 | agent-skills 仓库是昇腾（Ascend）社区用于AI辅助研发的核心管理仓库，专注于AI Agent技能的开发和管理，促进AI Agent技能的协同开发和创新。 |
| `slime-ascend` | 26 | 44 | 2026-03-03 |  |
| `docs` | 13 | 54 | 2026-01-12 | docs仓库用于介绍昇腾（Ascend）社区通用性文档 |
| `ascend-agreements` | 12 | 0 | 2026-04-14 | Ascend 迁移协议签署 |
| `infrastructure` | 11 | 19 | 2025-08-23 |  |
| `.gitcode` | 4 | 2 | 2026-08-11 | 可用于对 Ascend 进行全局 Issue 和 Pull Request 模板配置，提升用户反馈问题和贡献代码的体验。提供通用模板，支持项目通过特定目录定制模板，且项目模板优先级 |
| `release-management` | 1 | 14 | 2026-03-04 | 版本发布管理仓库，统一版本的管控规范，明确版本发布的全流程。 |

### 集群 / ModelZoo / CI 基建（7）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `mind-cluster` | 199 | 219 | 2025-12-30 | MindCluster 组件代码仓 |
| `ModelZoo-PyTorch` | 83 | 125 | 2025-11-16 |  |
| `mindcluster-deploy` | 82 | 57 | 2025-12-31 | 配合MindCluster基础组件使用的样例库，稳定版本请使用Tag中的代码 |
| `modelzoo-GPL` | 15 | 24 | 2025-11-16 |  |
| `perf-reference-ascend` | 11 | 29 | 2026-04-02 | 昇腾基础性能测试参考设计。提供perftest、xpu-perf等社区基础性能测试项目在昇腾NPU上适配参考。 |
| `modelzoo` | 7 | 6 | 2025-11-16 | Ascend ModelZoo |
| `ci-infra` | 6 | 7 | 2025-11-14 | ci-infra仓库用于介绍昇腾（Ascend）社区各项目持续集成（Continuous Integration）和持续发布（Continuous Delivery）的实施过程和要 |

### 推理引擎与服务化（MindIE）（6）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `MindIE-LLM` | 137 | 242 | 2025-12-21 | 昇腾自研大模型推理引擎 |
| `MindIE-SD` | 119 | 179 | 2026-09-09 | 昇腾亲和的多模态加速系列套件，现已支持vLLM Omni，Diffusers+CacheDit，lightx2v等框架。 |
| `MindInferenceService` | 55 | 31 | 2025-12-29 | MindInferenceService |
| `MindIE-Motor` | 54 | 178 | 2026-07-23 | 昇腾自研推理集群管理框架 |
| `MindIE-Motor-CPP` | 37 | 80 | 2026-07-09 | 昇腾自研推理集群管理框架 |
| `MindIE-Turbo` | 15 | 10 | 2025-12-09 | 昇腾大语言模型推理引擎加速库 |

### 编译器 / IR / Triton（5）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `triton-ascend` | 189 | 358 | 2026-05-18 | Triton Ascend 已经迁移到https://github.com/triton-lang/triton-ascend |
| `triton-ascend-kernels` | 29 | 313 | 2026-02-14 | triton-ascend-kernels |
| `ascendc-kernelgen-data` | 22 | 30 | 2026-03-03 | 提供用于昇腾 AscendC 算子代码生成的训练数据集，数据集涵盖多种算子类型，旨在支持算子代码自动生成模型的训练与评估。 |
| `llvm-project` | 3 | 52 | 2025-11-25 | llvm-project是一个模块化、可复用的编译器及工具链技术的集合。此fork用于添加昇腾上编译器的功能，支持AscendNPU IR等项目。 |
| `libdevice` | 2 | 14 | 2026-05-19 | libdevice |

### 通信 / 内存池化（3）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `memfabric_hybrid` | 178 | 126 | 2026-06-06 | 内存池化基础软件, 基于超节点总线、服务器网络实现DRAM与显存混合池化，提供极简的内存访问接口和高性能的内存直接访问能力，支撑多种场景下的数据共享与传输 |
| `memcache` | 154 | 98 | 2026-01-26 | MemCache是针对AI推理场景设计的高性能分布式KVCache缓存，针对昇腾超节点、服务器的实现了精细化性能调优，提供较好的High Availability能力,  同时对接 |
| `community` | 33 | 295 | 2025-11-04 | community 仓库是昇腾（Ascend）社区的核心管理仓库，用于实现组织级权限的统一管理。通过层级化的目录结构和配置文件，实现对项目、SIG组、代码仓库及成员权限的规范化管理 |

### 行业 / 领域 SDK（2）

| 仓库 | ★ | fork | 最后更新 | 说明 |
|---|---|---|---|---|
| `faiss` | 16 | 17 | 2026-03-25 | fork开源faiss，提供向量检索NPU加速能力。 |
| `text-embeddings-inference` | 5 | 14 | 2026-03-25 | fork开源text-embeddings-inference，提供昇腾NPU加速能力。 |

## 三、GitHub 组织 `Ascend`（112 个，镜像为主）

| 仓库 | ★ | fork | 最后 push | 语言 | 说明 |
|---|---|---|---|---|---|
| `pytorch` | 582 | 97 | 2026-09-30 | Python | Ascend PyTorch adapter (torch_npu). Mirror of https://gitcode.com/Ascend/pytorch |
| `samples` | 167 | 47 | 2023-11-22 | Python |  |
| `TransferQueue` | 158 | 52 | 2026-09-24 | Python | An asynchronous streaming data management module for efficient post-training. |
| `triton-ascend` | 129 | 18 | 2026-05-18 | MLIR | Triton adapter for Ascend. Mirror of https://gitcode.com/ascend/triton-ascend |
| `AscendSpeed` | 79 | 5 | 2023-12-15 | Python |  |
| `ModelZoo-PyTorch` | 77 | 9 | 2023-12-16 | Python |  |
| `cann-container-image` | 68 | 23 | 2026-09-28 | Dockerfile | Dockerfiles for Ascend CANN |
| `MindSpeed-LLM` | 60 | 23 | 2026-09-30 | Python |  |
| `MindSpeed-RL` | 60 | 5 | 2026-05-20 | Python |  |
| `AscendNPU-IR` | 57 | 30 | 2026-09-30 | C++ | Mirror of https://gitcode.com/Ascend/AscendNPU-IR |
| `MindSpeed-MM` | 51 | 31 | 2026-09-30 | Python |  |
| `agent-skills` | 47 | 2 | 2026-05-07 | Python |  |
| `modelzoo` | 29 | 5 | 2023-06-11 | - |  |
| `MindIE-LLM` | 28 | 8 | 2026-09-23 | C++ |  |
| `torchair` | 28 | 9 | 2026-06-08 | Python |  |
| `MindSpeed` | 26 | 10 | 2026-09-30 | Python |  |
| `triton-ascend-ops` | 23 | 21 | 2026-09-29 | Python |  |
| `tools` | 23 | 4 | 2023-06-11 | Python |  |
| `sglang` | 22 | 19 | 2026-09-30 | Python | SGLang is a high-performance serving framework for large language models and mul |
| `DrivingSDK` | 19 | 3 | 2026-06-08 | C++ |  |
| `docs` | 18 | 26 | 2026-09-30 | Python | The repository provides docs & api & tutorials & FAQ and all things like that. |
| `DeepSpeed` | 17 | 0 | 2023-12-05 | Python |  |
| `ray-ascend` | 16 | 5 | 2026-07-03 | Python | This is the official **live** mirror of Ascend-native hardware plugin for ray |
| `MindIE-SD` | 15 | 5 | 2026-09-30 | C++ |  |
| `ModelZoo-TensorFlow` | 14 | 3 | 2023-11-29 | Python |  |
| `op-plugin` | 13 | 4 | 2026-09-30 | Python |  |
| `mind-cluster` | 13 | 5 | 2026-09-30 | Go |  |
| `memcache` | 12 | 4 | 2026-06-06 | C++ |  |
| `Ascend-CI` | 11 | 6 | 2026-09-11 | Dockerfile | CI system for Ascend |
| `msmodelslim` | 8 | 3 | 2026-09-30 | Python |  |
| `mindspore` | 8 | 1 | 2022-07-19 | C++ |  |
| `memfabric_hybrid` | 7 | 4 | 2026-06-08 | C++ |  |
| `transformers` | 7 | 0 | 2023-11-09 | Python |  |
| `ascend_community_projects` | 6 | 0 | 2022-12-16 | Python |  |
| `msprobe` | 5 | 1 | 2026-09-30 | Python |  |
| `msinsight` | 4 | 0 | 2026-09-30 | C++ |  |
| `AgentSDK` | 4 | 1 | 2026-09-30 | Python |  |
| `graphengine` | 4 | 1 | 2021-11-14 | C++ |  |
| `RecSDK` | 3 | 2 | 2026-09-30 | C++ |  |
| `MindIE-Motor` | 3 | 5 | 2026-09-30 | Python |  |

（只列前 40，全量见本文件生成脚本 `C:/Users/华为/AppData/Local/Temp/gitcode_orgs.py` 与数据 `C:/Users/华为/attack/gitcode_orgs.json`、`orgs_probe.json`）
