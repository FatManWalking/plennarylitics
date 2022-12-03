	<!-- Required chart.js -->
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

	<!-- Chart line -->
	<script>
		const labels = ['January', 'February', 'March', 'April', 'May', 'June'];
		const data = {
			labels: labels,
			datasets: [
				{
					label: 'My First dataset',
					backgroundColor: 'hsl(252, 82.9%, 67.8%)',
					borderColor: 'hsl(252, 82.9%, 67.8%)',
					data: [0, 10, 5, 2, 20, 30, 45]
				}
			]
		};

		const configLineChart = {
			type: 'line',
			data,
			options: {}
		};

		var chartLine = new Chart(document.getElementById('chartLine'), configLineChart);
	</script>

<div class="grid grid-cols-3">
	<div class="carousel carousel-center rounded-box">
		<div id="slide1" class="carousel-item relative w-full">
			<div class="card lg:card-side bg-base-100 shadow-xl">
				<figure>
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olaf_Scholz_In_March_2022.jpg/220px-Olaf_Scholz_In_March_2022.jpg"
						alt="Scholz"
					/>
				</figure>
				<div class="card-body">
					<h2 class="card-title">Neuer Kanzler!</h2>
					<p>Was soll das.</p>
					<div class="card-actions justify-end">
						<button class="btn btn-primary">Mehr</button>
					</div>
				</div>
			</div>
			<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
				<a href="#slide4" class="btn btn-circle">❮</a>
				<a href="#slide2" class="btn btn-circle">❯</a>
			</div>
		</div>
		<div id="slide2" class="carousel-item relative w-full">
			<div class="card lg:card-side bg-base-100 shadow-xl">
				<figure>
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olaf_Scholz_In_March_2022.jpg/220px-Olaf_Scholz_In_March_2022.jpg"
						alt="Scholz"
					/>
				</figure>
				<div class="card-body">
					<h2 class="card-title">Kanzler im Fokus!</h2>
					<p>Hat jemand meinen Focus gesehen?</p>
					<div class="card-actions justify-end">
						<button class="btn btn-primary">Mehr</button>
					</div>
				</div>
			</div>
			<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
				<a href="#slide1" class="btn btn-circle">❮</a>
				<a href="#slide3" class="btn btn-circle">❯</a>
			</div>
		</div>
		<div id="slide3" class="carousel-item relative w-full">
			<div class="card lg:card-side bg-base-100 shadow-xl">
				<figure>
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olaf_Scholz_In_March_2022.jpg/220px-Olaf_Scholz_In_March_2022.jpg"
						alt="Scholz"
					/>
				</figure>
				<div class="card-body">
					<h2 class="card-title">Ah da ist mein Focus!</h2>
					<p>Warum riecht das hier so.</p>
					<div class="card-actions justify-end">
						<button class="btn btn-primary">Mehr</button>
					</div>
				</div>
			</div>
			<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
				<a href="#slide2" class="btn btn-circle">❮</a>
				<a href="#slide4" class="btn btn-circle">❯</a>
			</div>
		</div>
		<div id="slide4" class="carousel-item relative w-full">
			<div class="card lg:card-side bg-base-100 shadow-xl">
				<figure>
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olaf_Scholz_In_March_2022.jpg/220px-Olaf_Scholz_In_March_2022.jpg"
						alt="Scholz"
					/>
				</figure>
				<div class="card-body">
					<h2 class="card-title">Ich bin müde!</h2>
					<p>Ich mache ein Nickerchen im Kofferraum.</p>
					<div class="card-actions justify-end">
						<button class="btn btn-primary">Mehr</button>
					</div>
				</div>
			</div>
			<div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
				<a href="#slide3" class="btn btn-circle">❮</a>
				<a href="#slide1" class="btn btn-circle">❯</a>
			</div>
		</div>
	</div>

	<div />
	<div />

    <div class="shadow-lg rounded-lg overflow-hidden">
  <div class="py-3 px-5 bg-gray-50">Line chart</div>
  <canvas class="p-10" id="chartLine"></canvas>
</div>


</div>
