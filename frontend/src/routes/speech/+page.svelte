<script lang="ts">
	import { change_color } from '$lib/utils';
	import { parties } from '$lib/stores/parties.store';
	import { isDark } from '$lib/stores/theme.store';
	import Datepicker from '$lib/daisy/date.svelte';
	import { title } from '$lib/stores/title.store';
	import { onMount, onDestroy } from 'svelte';
	import Display from './display.svelte';

	// On mount set title to 'Speeches'
	onMount(() => {
		title.set('Redensuche');
		textcolor = change_color(!$isDark);
	});

	// On destroy set title to 'Plenarylitics'
	onDestroy(() => {
		title.set('Plenarylitics');
	});

	let textcolor: string;

	$: $isDark, (textcolor = change_color($isDark));

	let from_date: Date = new Date(1970); // In case user does not select a date (default: 1970)
	let to_date: Date = new Date(); // In case user does not select a date (default: today)

	// If User clicks 'search' button, set active_filter to true and display results
	let active_filter = {
		active: false,
		keyword: '',
		party: '',
		speaker: '',
		from_date,
		to_date
	};

	// If User clicks 'search' button, set active_filte
	function reset() {
		active_filter = {
			active: false,
			keyword: '',
			party: '',
			speaker: '',
			from_date: new Date(),
			to_date: new Date()
		};
	}

	// If User clicks 'search' button, go to /results with active_filter as query
</script>

{#if active_filter.active}
	<Display bind:active_filter />
{:else}
	<div
		class="hero min-h-screen"
		style="background-image: url(https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233);"
	>
		<div class="hero-overlay bg-opacity-60 w-full h-full" />
		<div class="hero-content w-full h-full">
			{#key $isDark}
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
									bind:value={active_filter.keyword}
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
									bind:value={active_filter.speaker}
								/>
							</div>
						</div>
					</div>
					<div class="card w-full glass {textcolor}">
						<div class="card-body items-center text-center">
							<h2 class="card-title">Partei</h2>
							<p>Suche nach Reden basierend auf der vortragenden Partei</p>
							<div class="form-control w-full max-w-xs">
								<select class="select select-bordered {textcolor}" bind:value={active_filter.party}>
									<option disabled selected>Partei wählen</option>
									{#each parties as party}
										<option value={party.technicalName}>{party.name}</option>
									{/each}
								</select>
							</div>
						</div>
					</div>
					<Datepicker {textcolor} bind:from_date bind:to_date />
					<div class="col-span-2 items-stretch ">
						<button
							class="btn btn-primary btn-lg w-full"
							on:click={() => {
								console.log('clicked');
								active_filter.active = true;
								active_filter.from_date = from_date;
								active_filter.to_date = to_date;
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
			{/key}
		</div>
	</div>
{/if}
