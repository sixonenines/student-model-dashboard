export type ModelType = "AFM" | "PFM" | "IFM";

export interface CoefficientEntry {
  feature: string;
  coef: number;
}

export interface PredictionEntry {
  row: number;
  predicted_probability: number;
  prediction: number;
}

export interface ModelStats {
  model_type: string;
  aic: number;
  aicc: number;
  bic: number;
  num_parameters: number;
  likelihood: number;
  brier_score: number;
  log_loss: number;
  rmse: number;
  acc_cv: number;
  precision: number;
  recall: number;
  f1: number;
}

export interface ModelResult {
  stats: ModelStats;
  coefficients: CoefficientEntry[];
  predictions: PredictionEntry[];
}

export interface PythonTrainResponse {
  models: Record<string, ModelResult>;
}

export interface RTrainResponse {
  stats: ModelStats;
  coefficients: CoefficientEntry[];
  predictions: PredictionEntry[];
}

export interface ValidateResponse {
  valid: boolean;
  errors: string[];
}

export interface TrainingState {
  loading: boolean;
  error: string | null;
  pythonResults: Record<string, ModelResult> | null;
  rResults: Record<string, ModelResult> | null;
}
