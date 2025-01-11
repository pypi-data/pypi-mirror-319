import type { FileData } from "@modelly/client";

export interface GalleryImage {
	image: FileData;
	caption: string | null;
}

export interface GalleryVideo {
	video: FileData;
	caption: string | null;
}
