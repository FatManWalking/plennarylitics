<script lang="ts">
	import { isDark } from '$lib/stores/theme.store';
	const textcolor = isDark ? 'text-neutral-900' : 'text-neutral-100';

	import * as Pancake from '@sveltejs/pancake';
	import { spring } from 'svelte/motion';
	import { onMount } from 'svelte';
	import data_mock from './data.js';

	import Form from '$lib/daisy/form.svelte';
	import { post, get } from '$lib/api';
	import type { ESDocument, ESResult } from '$lib/types';

	//FusionCharts
	import Charts from 'fusioncharts/fusioncharts.charts';
	import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
	import FusionCharts from 'fusioncharts';
	import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

	fcRoot(FusionCharts, Charts, FusionTheme);

	// use active filter as body for get request
	async function search() {
		const data: ESResult = await get('missing_mp/Corinna');

		let found_speeches: ESDocument[] = data.hits.hits;
		console.log(found_speeches);

		return found_speeches;
	}

	let query: ESResult;
	onMount(async () => {
		const res = await get(`missing_mp/Corinna`);
		console.log(res);
	});

	let selected_party: string = 'Alle';

	const chooseParty = () => {
		console.log('party chosen');
	};

	let dataSource = {
		chart: {
			caption: 'Fehlende Repräsentanten',
			subcaption: 'in der 20. Legislaturperiode',
			showValues: '0',
			showPercentInTooltip: '1',
			numberPrefix: '',
			enableMultiSlicing: '1',
			theme: 'fusion'
		},
		data: [
			{
				label: 'AFD',
				value: '12'
			},
			{
				label: 'AFD fehlt',
				value: '8'
			}
		]
	};
	let chartConfig = {
		type: 'pie2d',
		width: '100%',
		height: '100%',

		renderAt: 'chart-container',
		dataSource: dataSource
	};
</script>

<div
	class="hero max-h-screen"
	style="background-image: url(https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233);"
>
	<div class="hero-overlay bg-opacity-60" />
	<div class="hero-content text-center underline decoration-4 text-xl font-semibold text-teal-100">
		<h1 class="uppercase">Fehlende Repräsentanten</h1>
	</div>
</div>

<div class="pb-4">
	<Form bind:selected={selected_party} />
</div>

<div id="chart-container">
	<SvelteFC {...chartConfig} />
</div>

<style>
</style>
