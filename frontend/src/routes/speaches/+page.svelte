<script lang="ts">
	import Card from '$lib/daisy/card.svelte';
	import { Dropdown, DropdownItem, DropdownDivider, DropdownHeader } from 'flowbite-svelte';
	import { ButtonGroup, Button } from 'flowbite-svelte';

	import { goto } from '$app/navigation';

	const preserveScroll = (url: string) => {
		goto(url, {
			noScroll: true
		});
	};

	import { isDark } from '$lib/stores/theme.store';

	const textcolor = isDark ? 'text-neutral-900' : 'text-neutral-100';
</script>

<div
	class="hero max-h-screen"
	style="background-image: url(https://assets.deutschlandfunk.de/FILE_bee61ad621284fe91efe0037638b78b3/1920x1080.jpg?t=1597611045233);"
>
	<div class="hero-overlay bg-opacity-60" />
	<div class="hero-content text-center underline decoration-4 text-xl font-semibold text-teal-100">
		<h1 class="uppercase">Redensuche</h1>
	</div>
</div>

<div class="grid justify-items-end grid-cols-3 gap-2">
	<div class="form-control col-span-2 w-full">
		<div class="input-group ">
			<input type="text" placeholder="Search…" class="input input-bordered" />
			<button class="btn btn-square"> ▼ </button>

			<button class="btn btn-square"> 🔍 </button>
			<ButtonGroup>
				<Button>Proflie</Button>
				<Button>Settings</Button>
				<Button>Messages</Button>
			</ButtonGroup>
		</div>
	</div>
</div>

<div class="overflow-x-auto">
	<table class="table table-zebra w-full">
		<!-- head -->
		<thead>
			<tr>
				<th />
				<th>Name</th>
				<th>Job</th>
				<th>Favorite Color</th>
			</tr>
		</thead>
		<tbody>
			<!-- row 1 -->
			<tr>
				<th>1</th>
				<td>Cy Ganderton</td>
				<td>Quality Control Specialist</td>
				<td>Blue</td>
			</tr>
			<!-- row 2 -->
			<tr>
				<th>2</th>
				<td>Hart Hagerty</td>
				<td>Desktop Support Technician</td>
				<td>Purple</td>
			</tr>
			<!-- row 3 -->
			<tr>
				<th>3</th>
				<td>Brice Swyre</td>
				<td>Tax Accountant</td>
				<td>Red</td>
			</tr>
		</tbody>
	</table>
</div>
