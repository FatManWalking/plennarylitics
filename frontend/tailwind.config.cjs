/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}', "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",],
	theme: {
		extend: {}
	},
	plugins: [require('daisyui', 'tw-elements/dist/plugin', 'flowbite/plugin')]
};
