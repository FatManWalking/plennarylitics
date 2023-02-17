
const BACKEND_URL = process.env['BACKEND_URL'] as string;

export async function postContent(
	path: string,
	content: object,
	
): Promise<unknown> {
	const baboUrl = new URL(path, BACKEND_URL);

    // Neeed to use post otherwise the backend will return a error using a body
	const res = await fetch(baboUrl, {
		method: 'POST',
		body: JSON.stringify(content)
	});

	if (res.headers.get('content-type')?.includes('application/json')) {
		return await res.json();
	} else {
		console.error(`expected content type json, got ${res.headers.get('content-type')} instead`);
		return null;
	}
}