import { getEnvVariable } from '$lib/utils';
import { prerendering } from '$app/environment';
import { join } from 'path';

let BABO_URL = process.env['BABO_URL'] as string;

if (!prerendering && BABO_URL === undefined) {
	BABO_URL = getEnvVariable('VITE_BABO_URL') as string;
	if (BABO_URL === undefined) {
		console.warn(`missing env variable VITE_BABO_URL or BABO_URL`);
		process.exit(1);
	}
	console.warn(`using fallback BABO_URL=${BABO_URL}`);
}

export async function getContent(path: string): Promise<unknown> {
	const baseUrl = new URL(BABO_URL);
	const baboUrl = new URL(join(baseUrl.pathname, path), baseUrl);
	try {
		const res = await fetch(baboUrl, {
			headers: {
				'Content-Type': 'application/json',
				Accept: 'application/json',
				Authorization: `Bearer <todo>`
			}
		});

		return await res.json();
	} catch (e) {
		console.error(`failed to fetch (${baboUrl}):`, e);
	}
}

export async function postContent(path: string, content: object): Promise<unknown> {
	const baboUrl = new URL(path, BABO_URL);

	const res = await fetch(baboUrl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
			Authorization: `Bearer <todo>`
		},
		body: JSON.stringify(content)
	});

	return res;
}
