<!-- Path: frontend/src/routes/speech/display.svelte -->
<script lang="ts">
	import Time from 'svelte-time';

	import { post, get } from '$lib/api';
	import type { ESDocument, ESResult } from '$lib/types';

	// get the active filter from the query
	export let active_filter: {
		active: boolean;
		keyword: string;
		party: string;
		speaker: string;
		from_date: Date;
		to_date: Date;
	};

	console.log(active_filter);

	// the rsult currently displayed
	let currentSpeech: number = 0;

	// use active filter as body for get request
	async function queryES() {
		// 	// get the result from the backend
		//const data: ESResult = await get('test/Krankenhäuser');

		let query = 'speeches?';
		//create query for request
		for (let key in active_filter) {
			// from_date or to_date
			if (key == 'active') continue;
			else if (key == 'from_date' || key == 'to_date') {
				query +=
					key +
					'=' +
					// date of format yyyy-mm-dd
					active_filter[key].toISOString().slice(0, 10) +
					'&';
			} else if (active_filter[key] != '') {
				query += key + '=' + active_filter[key] + '&';
			}
		}
		//remove last '&'
		query = query.slice(0, -1);

		const data: ESResult = await get(query);

		let found_speeches: ESDocument[] = data.hits.hits;
		console.log(found_speeches);

		return found_speeches;
	}

	let query = queryES();

	// onMount(() => {
	// 	search();
	// });
</script>

<!-- Site to display the queried documents and provide a reader for a specific selected one-->
<!-- Info on how many been found and button to reset filter -->
<div class="flex flex-row gap-4 content-evenly">
	{#await query}
		<p>Waiting for your results. Please be patient</p>
	{:then result}
		{#if result.length > 0}
			<div class="basis-1/3 shrink-0">
				<div class="stats shadow w-full">
					<div class="stat">
						<div class="stat-figure text-secondary">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								class="inline-block w-8 h-8 stroke-current"
								><path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
								/></svg
							>
						</div>
						<div class="stat-title">Reden</div>
						<div class="stat-value">{result.length}</div>
						<div class="stat-desc">gefunden</div>
						<div class="stat-actions">
							<button class="btn btn-sm btn-success" on:click={() => (active_filter.active = false)}
								>Zurück zum Filter</button
							>
						</div>
					</div>
				</div>
				<!-- List all speeches on the left and display the current one on the right -->
				<div class="h-full w-full carousel carousel-vertical rounded-box">
					{#each result as speech, i}
						<div class="carousel-item w-full py-4 px-4">
							<div class="stats bg-primary text-primary-content">
								<div class="stat">
									<div class="stat-title">Redner</div>
									<div class="stat-value text-base">{speech._source.Sprecher}</div>
									<div class="stat-actions">
										<button
											class="btn btn-sm btn-success"
											on:click={(e) => {
												currentSpeech = i;
											}}>Mehr lesen</button
										>
									</div>
								</div>

								<div class="stat">
									<div class="stat-title">Partei</div>
									<div class="stat-value text-base">{speech._source.Partei}</div>
								</div>

								<div class="stat">
									<div class="stat-title">Datum</div>
									<div class="stat-value text-base"><Time timestamp={speech._source.Datum} /></div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
			{#key currentSpeech}
				<div class="card w-full bg-neutral overflow-auto">
					<div class="hero-content text-center text-neutral-content">
						<div class="">
							<h1 class="mb-5 text-xl font-bold">
								{result[currentSpeech]._source.Sprecher} am <Time
									timestamp={result[currentSpeech]._source.Datum}
								/>
							</h1>
							<p class="mb-5">{result[currentSpeech]._source.Text}</p>
						</div>
					</div>
				</div>
			{/key}
		{:else}
			<div class="basis-2/3 shrink-0 w-full">
				<div class="card glass">
					<div class="hero-content text-center text-neutral-content">
						<h1 class="mb-5 text-5xl font-bold">Ruhe.</h1>
						<p class="mb-5">
							Dein Suchergebis ist leider so leer wie dieser Bundestag. Versuche es doch mit einem
							anderen Filter.
						</p>
						<button class="btn btn-primary">Zurück zum Filter</button>
					</div>
				</div>
			</div>
		{/if}
	{/await}
</div>
