<script lang="ts">
	function validate() {
		console.log("I'm the validate() function");
	}

	export let selected: string = 'Alle';

	let options = [
		{ value: 'Alle', label: 'Alle' },
		{ value: 'CDU/CSU', label: 'CDU/CSU' },
		{ value: 'SPD', label: 'SPD' },
		{ value: 'Die Grünen', label: 'Die Grünen' },
		{ value: 'Die Linke', label: 'Die Linke' },
		{ value: 'FDP', label: 'FDP' },
		{ value: 'AFD', label: 'AFD' },
		{ value: 'Andere', label: 'Andere' }
	];
</script>

<form on:submit|preventDefault={validate} class="form-control">
	<div class="input-group">
		<select class="select select-bordered" bind:value={selected}>
			<option disabled>Filter nach Parteien</option>
			{#each options as option}
				<option value={option.value}>{option.label}</option>
			{/each}
		</select>
		<button class="btn" on:click={() => console.log()}>Go</button>
	</div>
</form>
