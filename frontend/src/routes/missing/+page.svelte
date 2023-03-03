<script lang="ts">
	import { isDark } from '$lib/stores/theme.store';
	import { change_color } from '$lib/utils';
	import { onMount } from 'svelte';
	import { onDestroy } from 'svelte';
	import Form from '$lib/daisy/form.svelte';
	import { post, get } from '$lib/api';
	import { title } from '$lib/stores/title.store';
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
	let textcolor: string;
	// On mount set title to 'Speeches'
	onMount(async () => {
		title.set('Fehlende Repräsentanten');
		textcolor = change_color(!$isDark);
		const res = await get(`missing_mp/Corinna`);
		console.log(res);
	});

	// On destroy set title to 'Plenarylitics'
	onDestroy(() => {
		title.set('Plenarylitics');
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
		width: '400',
		height: '400',

		renderAt: 'chart-container',
		dataSource: dataSource
	};
</script>

<div
	class="hero max-h-screen"
	style="background-image: url(https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233);"
>
	<div class="hero-overlay bg-opacity-60" />
	<div class="hero-content">
		<div class="pb-4">
			<Form bind:selected={selected_party} />
		</div>

		<div id="chart-container">
			<SvelteFC {...chartConfig} />
		</div>
	</div>
</div>
