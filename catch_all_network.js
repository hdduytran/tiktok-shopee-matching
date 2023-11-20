(async () => {
    const getContent = r => r.url() && !r.url().startsWith('data:') && r.contentData();
    const nodes = UI.panels.network.networkLogView.dataGrid.rootNode().flatChildren();
    const requests = nodes.map(n => n.request());
    const contents = await Promise.all(requests.map(getContent));
    const looks = contents.map((data, i) => {
      const r = requests[i];
      const url = r.url();
      const content = data
      return JSON.parse(content.content);
    });
    looks
    // console.log(looks);
  })();

w