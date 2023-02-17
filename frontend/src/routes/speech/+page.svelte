<script lang="ts">
	import { change_color, preserveScroll } from '$lib/utils';
	import { parties } from '$lib/stores/parties.store';
	import { isDark } from '$lib/stores/theme.store';
	import Datepicker from '$lib/daisy/date.svelte';
	import { title } from '$lib/stores/title.store';
	import { onMount, onDestroy } from 'svelte';

	// On mount set title to 'Speeches'
	onMount(() => {
		title.set('Redensuche');
	});

	// On destroy set title to 'Plenarylitics'
	onDestroy(() => {
		title.set('Plenarylitics');
	});

	let textcolor: string;

	$: $isDark, (textcolor = change_color($isDark));

	let keyword = '';
	let party = 'Partei wählen';
	let speaker = '';

	let from_date: Date = new Date();
	let to_date: Date = new Date();

	// If User clicks 'search' button, set active_filter to true and display results
	let active_filter = {
		active: false,
		keyword,
		party,
		speaker,
		from_date,
		to_date
	};
</script>

<div
	class="hero max-h-screen"
	style="background-image: url(https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233);"
>
	<div class="hero-overlay bg-opacity-60" />
	<div class="hero-content">
		{#key $isDark}
			{#if !active_filter.active}
				<div class="grid justify-items-center grid-cols-2 gap-2 py-4 px-4 sm:grid-cols-1 ">
					<div class="card w-full glass {textcolor}">
						<div class="card-body items-center text-center">
							<h2 class="card-title">Themen</h2>
							<p>Suche nach Reden basiernd auf Schlüsselwörtern die in ihnen enthalten sind.</p>
							<div class="form-control w-full max-w-xs">
								<input
									type="text"
									placeholder="Arbeitslosigkeit"
									class="input input-bordered w-full max-w-xs "
									bind:value={keyword}
								/>
							</div>
						</div>
					</div>
					<div class="card w-full glass {textcolor}">
						<div class="card-body items-center text-center">
							<h2 class="card-title">Redner</h2>
							<p>Suche nach Reden von bestimmten Personen</p>
							<div class="form-control w-full max-w-xs">
								<input
									type="text"
									placeholder="Olaf Scholz"
									class="input input-bordered w-full max-w-xs {textcolor}"
									bind:value={speaker}
								/>
							</div>
						</div>
					</div>
					<div class="card w-full glass {textcolor}">
						<div class="card-body items-center text-center">
							<h2 class="card-title">Partei</h2>
							<p>Suche nach Reden basierend auf der vortragenden Partei</p>
							<div class="form-control w-full max-w-xs">
								<select class="select select-bordered {textcolor}" bind:value={party}>
									<option disabled selected>Partei wählen</option>
									{#each parties as party}
										<option>{party.name}</option>
									{/each}
								</select>
							</div>
						</div>
					</div>
					<Datepicker {textcolor} {from_date} {to_date} />
					<div class="col-span-2 items-stretch ">
						<button
							class="btn btn-primary btn-lg w-full"
							on:click={() => {
								console.log('clicked');
								active_filter = {
									active: true,
									keyword,
									party,
									speaker,
									from_date,
									to_date
								};
							}}
						>
							Suche starten
						</button>
						<br />
						<small class="text-white-900"
							>Bitte beachten Sie das nicht alle Kategorien gleichzeitig funktionieren</small
						>
					</div>
				</div>
			{:else}
				<p>Placeholder</p>
			{/if}
		{/key}
	</div>
</div>
