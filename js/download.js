const getContent = r => {
    const url = r.url();
    // Using regex to test if the URL contains 'rcmd' or 'sold'
    const regex = /rcmd_item|filter_sold_out/;
    return url && regex.test(url) && r.contentData();
};

const nodes = UI.panels.network.networkLogView.dataGrid.rootNode().flatChildren();
const requests = nodes.map(n => n.request());
const contents = await Promise.all(requests.map(getContent));
const looks = contents.map((data, i) => {
    if (!data) return null; // Skip null data

    const r = requests[i];
    const url = r.url();
    console.log(url);
    const content = data;
    return JSON.parse(content.content);
}).filter(Boolean); // Filter out null values

const jsonString = JSON.stringify(looks, null, 2);
const blob = new Blob([jsonString], { type: 'application/json' });
const link = document.createElement('a');
link.download = 'all.json';
link.href = window.URL.createObjectURL(blob);
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
