<script lang="ts">
	// Import our global CSS
	import '$lib/global.css';

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
<footer class="footer p-10 bg-neutral text-neutral-content inset-x-0 bottom-0">
	<div>
		<span class="footer-title">Services</span>
		<a class="link link-hover">Branding</a>
		<a class="link link-hover">Design</a>
		<a class="link link-hover">Marketing</a>
		<a class="link link-hover">Advertisement</a>
	</div>
	<div>
		<span class="footer-title">Company</span>
		<a class="link link-hover">About us</a>
		<a class="link link-hover">Contact</a>
	</div>
	<div>
		<span class="footer-title">Legal</span>
		<a class="link link-hover">Terms of use</a>
		<a class="link link-hover">Privacy policy</a>
		<a class="link link-hover">Cookie policy</a>
	</div>
</footer>

<style>
</style>
