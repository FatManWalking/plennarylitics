<script lang="ts">
	// Our goal was to create a 2-layer donut chart with a legend.
	// The tools we used were Svelte, D3, and TailwindCSS on the frontend and the elastic search API on the backend.
	// We were not able to combine the two data formats the 2 sides expected. We tried to use the elastic search API to get the data in the format we needed, but we were not able to do so.

	// In theory the endpoints are available in the backend
	// We filled in with visualizations of the data we got from the kibana dashboard
	import { get, post } from '$lib/api';
	import { onMount, onDestroy } from 'svelte';
	import { isDark } from '$lib/stores/theme.store';
	import { preserveScroll, change_color } from '$lib/utils';
	import { title } from '$lib/stores/title.store';

	let textcolor: string;
	$: $isDark, (textcolor = change_color($isDark));

	onMount(async () => {
		title.set('Fehlende Abgeordnete');
		const response = await get('get_missing_mps_by_party/CDU');
		console.log(response);
		textcolor = change_color(!$isDark);
	});

	onDestroy(() => {
		title.set('Plenarylitics');
	});

	// Here the fill in visuals from elasticsearch
	import { Card } from '$lib/daisy';
	const FDPvsAFD = new URL('$lib/assets/FDPvsAFD.png', import.meta.url).href;
	const LINKEtime = new URL('$lib/assets/LINKEtime.png', import.meta.url).href;
</script>

<div class="flex flex-col justify-center carousel carousel-center rounded-box pt-4 ">
	<div id="slide1" class="carousel-item relative w-fill">
		<Card klass={textcolor} link="/remarks">
			<figure slot="image">
				<img src={FDPvsAFD} alt="Vergleich zwischen FDP und AFD" />
			</figure>
			<h2 slot="title">
				Direktvergleich FDP und AFD
				<div class="badge badge-secondary">NEW</div>
			</h2>
			<p slot="description">
				Der Graph zeigt den direkten Vergleich zwischen der FDP und der AFD. Von allen Abgeordneten
				beider Parteien die fehlen, wieviel Prozent sind es bei der FDP und wieviel bei der AFD.
				Vorsicht dieser Vergleich ist nicht ganz korrekt, da die FDP und die AFD nicht gleich viele
				Abgeordnete haben und sollte nur als grobe Orientierung dienen.<br /> Die FDP hat 92 und die
				AFD 78 Abgeordnete. Es fehlt also ein gleich großer Teil beider Parteien wenn der Balken bei
				54% steht.
			</p>
		</Card>
		<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
			<a href="missing/#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/missing`)}
				>❮</a
			>
			<a href="missing/#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/missing`)}
				>❯</a
			>
		</div>
	</div>

	<div id="slide2" class="carousel-item relative w-fill">
		<Card klass={textcolor} link="/remarks">
			<figure slot="image">
				<img src={LINKEtime} alt="Fehlen der Linken Abgeordneten über Zeit" />
			</figure>
			<h2 slot="title">
				Fehlende Linke
				<div class="badge badge-secondary">NEW</div>
			</h2>
			<p slot="description">
				Der Graph zeigt wieviele Abgeordnete der Partei "Die Linke" in den letzten 15 Monaten nicht
				in den Sitzungen waren.
			</p>
			<p slot="button">Mehr erfahren</p>
		</Card>
		<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
			<a href="missing/#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/missing`)}
				>❮</a
			>
			<a href="missing/#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/missing`)}
				>❯</a
			>
		</div>
	</div>
</div>

<style>
</style>
