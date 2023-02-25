<!-- Path: frontend/src/routes/speech/display.svelte -->
<script lang="ts">
	import { change_color, preserveScroll } from '$lib/utils';
	import { parties } from '$lib/stores/parties.store';
	import { isDark } from '$lib/stores/theme.store';

	import Time, { svelteTime } from 'svelte-time';
	import { dayjs } from 'svelte-time';

	let time = dayjs().format('MMM DD, YYYY');

	interface Speech {
		speaker: string;
		text: string;
		party: string;
		date: Date;
	}

	let speeches: Speech[] = [
		{
			speaker: 'Max Mustermann',
			party: 'CDU',
			date: new Date(),
			text: 'Est at et at ut lorem eirmod nostrud lorem eu amet. Diam exerci elitr sit eum eos ut diam ad duo et sea stet. Sea kasd diam. Lorem iusto amet takimata. Justo magna amet at vero delenit odio option dolor. Diam est takimata eos delenit consetetur sit ipsum accusam dignissim at sed. Praesent lorem luptatum in dolor magna clita kasd ut dolore rebum nibh stet et diam duo diam in. Imperdiet aliquip blandit nulla eleifend odio dolore euismod. Accumsan sanctus tempor tempor et feugiat. Eros lobortis et duo voluptua accumsan vel accumsan nonumy kasd dolor. Eirmod eos option aliquyam voluptua ad. Sanctus lorem vulputate amet tempor odio consetetur lobortis tempor kasd consetetur eirmod invidunt amet dolor. Gubergren diam eros autem eirmod kasd no sed diam vero dolore facer magna no at kasd.At duis ut exerci labore et magna sit vero eos erat invidunt nulla justo minim iusto est vero labore. Clita sit diam dolor. Rebum tincidunt eos elitr erat esse labore veniam sed elitr ipsum sed clita eos ea dolores esse tempor imperdiet. Lorem sanctus eum erat no eirmod dolor gubergren eros nulla clita takimata diam commodo et sanctus nulla. Erat dolor amet clita ipsum sed rebum dolor nisl consectetuer justo dolores dolore sea duis. Kasd vel in consetetur. Ullamcorper et eos sit zzril erat at. Et lorem suscipit no enim tincidunt. Sit tempor no vulputate sed lorem labore.'
		},
		{
			speaker: 'Max Mustermann',
			party: 'CDU',
			date: new Date(),
			text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nunc nisl eu nunc.'
		}
	];

	let currentSpeech: Speech = speeches[0];
	function changeSpeech(speech: Speech) {
		currentSpeech = speech;
	}
</script>

<!-- Site to display the queried documents and provide a reader for a specific selected one-->
<!-- Info on how many been found and button to reset filter -->

{#if speeches.length > 0}
	<div class="grid grid-rows-4 justify-self-start">
		<div class="stats shadow">
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
				<div class="stat-value">{speeches.length}</div>
				<div class="stat-desc">gefunden</div>
				<div class="stat-actions">
					<button class="btn btn-sm btn-success">Zurück zum Filter</button>
				</div>
			</div>
		</div>
		<!-- List all speeches on the left and display the current one on the right -->
		<div class="row-span-3 h-full carousel carousel-vertical rounded-box">
			{#each speeches as speech, i}
				<div class="carousel-item w-full py-4">
					<div class="stats bg-primary text-primary-content">
						<div class="stat ">
							<div class="stat-title">Redner</div>
							<div class="stat-value text-base">{speech.speaker}</div>
							<div class="stat-actions">
								<button
									class="btn btn-sm btn-success"
									on:click={(e) => (changeSpeech(speeches[i]), console.log(currentSpeech.text))}
									>Mehr lesen</button
								>
							</div>
						</div>

						<div class="stat">
							<div class="stat-title">Partei</div>
							<div class="stat-value text-base">{speech.party}</div>
						</div>

						<div class="stat">
							<div class="stat-title">Datum</div>
							<div class="stat-value text-base"><Time timestamp={speech.date} /></div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
	{#key currentSpeech}
		<div class="card h-96 w-full bg-neutral my-4 overflow-auto">
			<div class="hero-content text-center text-neutral-content">
				<div class="max-w-md">
					<h1 class="mb-5 text-xl font-bold">
						{currentSpeech.speaker} am <Time timestamp={currentSpeech.date} />
					</h1>
					<p class="mb-5">{currentSpeech.text}</p>
				</div>
			</div>
		</div>
	{/key}
{:else}
	<div class="w-full py-4">
		<div class="card w-96 glass">
			<div class="hero-content text-center text-neutral-content">
				<div class="max-w-md">
					<h1 class="mb-5 text-5xl font-bold">Ruhe.</h1>
					<p class="mb-5">
						Dein Suchergebis ist leider so leer wie dieser Bundestag. Versuche es doch mit einem
						anderen Filter.
					</p>
					<button class="btn btn-primary">Zurück zum Filter</button>
				</div>
			</div>
		</div>
	</div>
{/if}
