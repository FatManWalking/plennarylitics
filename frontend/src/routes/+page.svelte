<script lang="ts">
	import Card from '$lib/daisy/card.svelte';
	import { preserveScroll, change_color } from '$lib/utils';
	import { isDark } from '$lib/stores/theme.store';
	import { onMount } from 'svelte';
	import { get } from '$lib/api';

	let textcolor: string;
	$: $isDark, (textcolor = change_color($isDark));

	onMount(async () => {
		const data: object = await get('');
		if (data.hasOwnProperty('plennarylitics')) {
			// reached backend
			// console.log(data);
		} else {
			// something went wrong
			console.log('something went wrong', data);
		}

		// trigger is dark mode
		$isDark = true;
	});
</script>

<div
	class="hero min-h-screen"
	style="background-image: url(https://www.bbr.bund.de/BBR/DE/Bauprojekte/Berlin/Politik/DBT/reichstagsgebaeude/Bilder/reichstag-frontale-teaser.jpg?__blob=poster&v=2);"
>
	<div class="hero-overlay bg-opacity-60" />
	<div class="hero-content text-center text-neutral-content">
		<div class="max-w-md">
			<h1 class="mb-5 text-5xl font-bold">Willkommen bei Plennarylitics</h1>
			<p class="mb-5">
				Hier findet du Informationen über die Plenardebatten des Deutschen Bundestages. Sauber und
				einfach aufbereitet.
			</p>

			<div class="carousel carousel-center rounded-box pt-4">
				<div id="slide1" class="carousel-item relative w-full">
					<Card klass={textcolor} link="/speech">
						<p slot="button">Zu den Reden</p>
					</Card>
					<div
						class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2"
					>
						<a href="#slide3" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❮</a>
						<a href="#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❯</a>
					</div>
				</div>

				<div id="slide2" class="carousel-item relative w-full">
					<Card klass={textcolor} link="/missing">
						<figure slot="image">
							<img
								src="https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233"
								alt="Leerer Bundestag"
							/>
						</figure>
						<h2 slot="title">
							Abwesende Abgeordnete
							<div class="badge badge-secondary">NEW</div>
						</h2>
						<p slot="description">
							Finde heraus, wie viele Abgeordnete an einer Debatte teilgenommen haben und wer
							besonders oft abwesend ist.
						</p>
						<p slot="button">Mehr erfahren</p>
					</Card>
					<div
						class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2"
					>
						<a href="#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❮</a>
						<a href="#slide3" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❯</a>
					</div>
				</div>

				<div id="slide3" class="carousel-item relative w-full">
					<Card klass={textcolor}>
						<figure slot="image">
							<img
								src="https://www.bundestag.de/resource/image/865170/16x9/624/351/d8a1b48fa67f30863d6ddd44ab2a39a1/6CB19B68D6099747545D197B19A7F4F3/kw42_konstituierende_sitzung_bild_bas_rede.jpg"
								alt="Leerer Bundestag"
							/>
						</figure>
						<h2 slot="title">
							Zwischenrufe
							<div class="badge badge-secondary">NEW</div>
						</h2>
						<p slot="description">
							Sieh dir an wer Monologe hält und wer sich durch Zwischenrufe durchsetzt.
						</p>
						<p slot="button">Mehr erfahren</p>
					</Card>
					<div
						class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2"
					>
						<a href="#slide2" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❮</a>
						<a href="#slide1" class="btn btn-circle" on:click={() => preserveScroll(`/`)}>❯</a>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- <div class="chat chat-start place-self-end">
		<div class="chat-image avatar">
			<div class="w-10 rounded-full">
				<img
					src="https://citizenz.de/wp-content/uploads/2019/08/ObiWan-696x349.jpg"
					alt="obi-wan"
				/>
			</div>
		</div>
		<div class="chat-bubble">It was said that you would, destroy the Sith, not join them.</div>
	</div> -->
</div>
