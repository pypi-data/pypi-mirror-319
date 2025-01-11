export { Client } from "./client";

export { predict } from "./utils/predict";
export { submit } from "./utils/submit";
export { upload_files } from "./utils/upload_files";
export { FileData, upload, prepare_files } from "./upload";
export { handle_file } from "./helpers/data";

export type {
	SpaceStatus,
	StatusMessage,
	Status,
	client_return,
	UploadResponse,
	RenderMessage,
	LogMessage,
	Payload,
	Config
} from "./types";

// todo: remove in @modelly/client v1.0
export { client } from "./client";
export { duplicate_space as duplicate } from "./client";
