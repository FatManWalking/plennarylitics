<script lang="ts">
	// Our goal was to create a 2-layer donut chart with a legend.
	// The tools we used were Svelte, D3, and TailwindCSS on the frontend and the elastic search API on the backend.
	// We were not able to combine the two data formats the 2 sides expected. We tried to use the elastic search API to get the data in the format we needed, but we were not able to do so.

	// In theory the endpoints are available in the backend
	// We filled in with visualizations of the data we got from the kibana dashboard

	import { quantize, interpolatePlasma, pie, arc } from 'd3';
	import data from './donut-data.js'; // or pass data to component as prop

	const width = 200; // the outer width of the chart, in pixels
	const height = width; // the outer height of the chart, in pixels
	const percent = false; // format values as percentages (true/false)
	const fontSize = 10; // the font size of the x and y values
	const strokeWidth = 2; // the width of stroke separating wedges
	const strokeLinejoin = 'round'; // line join style of stroke separating wedges
	const outerRadius = Math.min(width, height) * 0.4 - 60; // the outer radius of the circle, in pixels
	const innerRadius = 90; // the inner radius of the chart, in pixels
	const labelPosition = 0.5; // the position of the label offset from center
	const labelRadius = innerRadius * labelPosition + outerRadius * 0.6; // center radius of labels
	const strokeColorWOR = 'black'; //stroke color when inner radius is greater than 0
	const strokeColorWIR = 'black'; //stroke color when inner radius is 0
	const stroke = innerRadius > 0 ? strokeColorWIR : strokeColorWOR; // stroke separating widths
	const padAngle = stroke === 'none' ? 1 / outerRadius : 0; // angular separation between wedges

	const x = Object.keys(data[0])[0]; // given d in data, returns the (ordinal) x-value
	const y = Object.keys(data[0])[1]; // given d in data, returns the (quantitative) y-value
	const xVals = data.map((el) => el[x]);
	let yVals = data.map((el) => Number(el[y]));
	if (percent) {
		const total = yVals.reduce((a, b) => a + b, 0);
		yVals = yVals.map((el) => el / total);
	}
	const iVals = data.map((el, i) => i);

	// colors can be adjusted manually by creating a color array which length matches length of data set.
	let colors;
	if (!colors) colors = quantize((t) => interpolatePlasma(t * 0.7 + 0.3), xVals.length);

	const wedges = pie()
		.padAngle(padAngle)
		.sort(null)
		.value((i) => yVals[i])(iVals);

	const arcPath = arc().innerRadius(innerRadius).outerRadius(outerRadius);

	const arcLabel = arc().innerRadius(labelRadius).outerRadius(labelRadius);

	import { get, post } from '$lib/api';
	import { onMount, onDestroy } from 'svelte';
	import { isDark } from '$lib/stores/theme.store';
	import { preserveScroll, change_color } from '$lib/utils';
	import { title } from '$lib/stores/title.store';

	let textcolor: string;
	$: $isDark, (textcolor = change_color($isDark));

	onMount(async () => {
		title.set('Zwischenrufe');
		const response = await get('remarks');
		console.log(response);
		textcolor = change_color(!$isDark);
	});

	onDestroy(() => {
		title.set('Plenarylitics');
	});

	// Here the fill in visuals from elasticsearch
	import { Card } from '$lib/daisy';
	const RemarkByType = new URL('$lib/assets/RemarkByType.png', import.meta.url).href;
	const RemarksPartyParty = new URL('$lib/assets/RemarksPartyParty.png', import.meta.url).href;
</script>

<!-- <p>D3 demo</p>
<svg {width} {height} viewBox="{-width / 2} {-height / 2} {width} {height}">
	{#each wedges as wedge, i}
		<path
			fill={colors[i]}
			d={arcPath(wedge)}
			{stroke}
			stroke-width={strokeWidth}
			stroke-linejoin={strokeLinejoin}
		/>
		<g text-anchor="middle" transform="translate({arcLabel.centroid(wedge)})">
			<text font-size={fontSize}>
				<tspan font-weight="bold">{xVals[i]}</tspan>
				<tspan x="0" dy="1.1em"
					>{percent ? `${(yVals[i] * 100).toFixed(2)}%` : yVals[i].toLocaleString('en-US')}</tspan
				>
			</text>
		</g>
	{/each}
</svg> -->

<div class="flex flex-col justify-center carousel carousel-center rounded-box pt-4 ">
	<div id="slide1" class="carousel-item relative w-fill">
		<Card klass={textcolor} link="/remarks">
			<figure slot="image">
				<img src={RemarkByType} alt="Arten von Zwischenrufen" />
			</figure>
			<h2 slot="title">
				Zwischenrufe nach Art
				<div class="badge badge-secondary">NEW</div>
			</h2>
			<p slot="description">
				Diese Grafik zeigt dir wie viel Prozent der Zeit Parteien die Reden anderer Parteien
				kommentieren <br /> und in welcher Form sie das tun
			</p>
		</Card>
		<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
			<a href="remarks/#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/remarks`)}
				>❮</a
			>
			<a href="remarks/#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/remarks`)}
				>❯</a
			>
		</div>
	</div>

	<div id="slide2" class="carousel-item relative w-fill">
		<Card klass={textcolor} link="/remarks">
			<figure slot="image">
				<img src={RemarksPartyParty} alt="Zwischenrufe zwischen Parteien" />
			</figure>
			<h2 slot="title">
				Zwischenrufe zwischen Parteien
				<div class="badge badge-secondary">NEW</div>
			</h2>
			<p slot="description">
				Der innere Kreis zeigt dir welche Partei spricht und der äußere welche andere Partei die
				Rede unterbricht oder unterstützt
			</p>
			<p slot="button">Mehr erfahren</p>
		</Card>
		<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
			<a href="remarks/#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/remarks`)}
				>❮</a
			>
			<a href="remarks/#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/remarks`)}
				>❯</a
			>
		</div>
	</div>
</div>

<style>
</style>
