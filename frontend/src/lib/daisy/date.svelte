<script lang="ts">
	import { DateInput } from 'date-picker-svelte';
	export let from_date: Date = new Date();
	export let to_date: Date = new Date();
	export let textcolor = '';

	// Function to check "from" is "before" to date
	function check_dates() {
		console.log('check');
		if (from_date > to_date) {
			from_date = to_date;
		}
	}

	$: from_date, check_dates();
	$: to_date, check_dates();
</script>

<div class="card w-96 glass">
	<div class="card-body items-center text-center {textcolor}">
		<h2 class="card-title">Zeitraum</h2>
		<p>Suche nach Reden basierend auf einem Zeitraum</p>
		<div class="form-control max-w-xs">
			<!-- From -->
			<div class="grid grid-cols-2">
				<label for="from_date">Von:</label>
				<DateInput
					bind:value={from_date}
					format="dd.MM.yyyy"
					browseWithoutSelecting={true}
					closeOnSelection={true}
				/>
			</div>
			<!-- To -->
			<div class="grid grid-cols-2">
				<label for="to_date">Bis:</label>
				<DateInput
					bind:value={to_date}
					format="dd.MM.yyyy"
					browseWithoutSelecting={true}
					closeOnSelection={true}
				/>
			</div>
		</div>
	</div>
</div>
