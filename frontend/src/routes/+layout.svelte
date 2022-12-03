<script lang="ts">
	import Nav from '$lib/daisy/navbar.svelte';
	import { onMount } from 'svelte';
	import '../app.css';

	import { isDark } from '../lib/stores/theme.store';

	const THEMES = {
		DARK: 'business',
		LIGHT: 'garden'
	};

	onMount(async () => {
		document.documentElement.setAttribute('data-theme', $isDark ? THEMES.DARK : THEMES.LIGHT);
	});
</script>

<Nav />
<slot />

<style>
	/* :global(body) {
		background-color: lightseagreen;
		background-image: url('https://images.pexels.com/photos/956981/milky-way-starry-sky-night-sky-star-956981.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260');
	} */
</style>
