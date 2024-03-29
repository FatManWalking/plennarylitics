let BACKEND_URL = 'http://localhost:8080' as string;

export async function get<T>(path: string): Promise<T> {
	console.log(`getting from ${BACKEND_URL}/${path}`);
	const response = await fetch(`${BACKEND_URL}/${path}`, {
		method: 'GET',
		// Allowing CORS
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
			Origin: 'http://localhost',
			Referer: 'http://localhost'
		},
	});
	console.log(`response: ${response}`);
	return response.json();
}

export async function post<T>(path: string, body: any): Promise<T> {
	const response = await fetch(`${BACKEND_URL}/${path}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(body),
	});
	return response.json();
}