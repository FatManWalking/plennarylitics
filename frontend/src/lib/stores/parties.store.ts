// List of currently available parties to search for
type party = {
    name: string;
    color: string;
    id: number;
    technicalName: string;
};

export const parties: party[] = [
    {
        name: 'CDU / CSU',
        color: '#000000',
        id: 1,
        technicalName: 'CDU',
    },
    {
        name: 'SPD',
        color: '#E4002B',
        id: 2,
        technicalName: 'SPD',
    },
    {
        name: 'Bündnis 90 / GRÜNE',
        color: '#009D3E',
        id: 3,
        technicalName: 'Bündnis 90 /Die Grünen',
    },
    {
        name: 'FDP',
        color: '#FFCD00',
        id: 4,
        technicalName: 'FDP',
    },
    {
        name: 'AfD',
        color: '#00A1DE',
        id: 5,
        technicalName: 'AfD',
    },
    {
        name: 'Linke',
        color: '#FF6D00',
        id: 6,
        technicalName: 'Die Linke',
    },
    {
        name: 'Sonstige',
        color: '#808080',
        id: 7,
        technicalName: 'Fraktionslos',
    },
];
