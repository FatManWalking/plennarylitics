import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';


const config: UserConfig = {
	plugins: [sveltekit()],
	build: {
		minify: false,
	},
	server: {
		port: 3000,
		strictPort: true,
		https: false,
		watch: { usePolling: true },
		hmr: {
			clientPort: 3000,
		},
	},
};

export default config;
