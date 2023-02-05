<script lang="ts">
	export let link = '/test';
	export let klass = '';
</script>

<div class="card card-compact shadow-xl ">
	<figure>
		<slot name="image">
			<img
				src="https://www.bbr.bund.de/BBR/DE/Bauprojekte/Berlin/Politik/DBT/reichstagsgebaeude/Bilder/reichstag-frontale-teaser.jpg?__blob=poster&v=2"
				alt="Testbild"
			/>
		</slot>
	</figure>
	<div
		class="card-body items-center text-center font-semibold font-mono bg-base-100 {klass}"
	>
		<h2 class="card-title">
			<slot name="title">
				Olaf Scholz
				<div class="badge badge-secondary">NEW</div>
			</slot>
		</h2>
		<p>
			<slot name="description" class="bg-base-100">
				Olaf Scholz ist ein deutscher Politiker der SPD. Er ist seit dem 27. September 2017
				Bundesminister der Finanzen und seit dem 12. März 2021 Bundeskanzlerkandidat der SPD.
			</slot>
		</p>
		<div class="card-actions justify-end">
			<button on:click={() => (window.location.href = link)} class="btn btn-primary">
				<slot name="button">Mehr erfahren</slot>
			</button>
		</div>
	</div>
</div>
