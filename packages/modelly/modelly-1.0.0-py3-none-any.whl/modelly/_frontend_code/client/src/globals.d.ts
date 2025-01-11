import { ApiData, ApiInfo, Config } from "./types";

declare global {
	interface Window {
		__modelly_mode__: "app" | "website";
		modelly_config: Config;
		modelly_api_info: ApiInfo<ApiData> | { api: ApiInfo<ApiData> };
		__is_colab__: boolean;
		__modelly_space__: string | null;
	}
}
