# HERA fine-tune — training recap

- **Run**: `finetune_20260602T174128Z_db01ac`
  - base_model: Qwen/Qwen3-8B
  - max_seq_length: 3072
  - seed: 1337
- **Steps**: 27 | **epochs**: 3.0
- **Train loss**: 2.587 → 2.098
- **Eval loss**: 2.225 → 1.971 (best **1.971** @ step 27)
- ✅ eval_loss n'est pas reparti à la hausse → pas de signe net d'overfitting.

## Courbe train_loss
| step | train_loss |
|---:|---:|
| 10 | 2.5872 |
| 20 | 2.0984 |

## Eval
| step | eval_loss |
|---:|---:|
| 9 | 2.2252 |
| 18 | 2.0086 |
| 27 | 1.9709 |

- **Adapter**: 174.7 MB · r=16 α=32 dropout=0.05 · targets=['o_proj', 'gate_proj', 'up_proj', 'q_proj', 'down_proj', 'v_proj', 'k_proj']
