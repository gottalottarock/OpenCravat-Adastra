widgetGenerators['adastra'] = {
	'variant': {
		'width': 880, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Transcription factors',' ', tabName)
			var allMappings = getWidgetData(tabName, 'adastra', row, 'all_tf');
			if (allMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
			}
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Uniprot ID', 'Effect size Ref', 'Effect size Alt', 'Mean BAD', 'FDR Ref', 'FDR Alt', 'Motif concordance']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row_r = results[i];
					var uniprot_id = row_r[0];
					var uniprot_link = `https://www.uniprot.org/uniprot/${uniprot_id}`
					var tr = getWidgetTableTr([uniprot_link, row_r[1], row_r[2], row_r[3], row_r[4], row_r[5], row_r[6],], [uniprot_id]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
			addInfoLine(div, 'Cell types',' ', tabName)
			var allCLMappings = getWidgetData(tabName, 'adastra', row, 'all_cl');
			if (allCLMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
			}
			if (allCLMappings != undefined && allCLMappings != null) {
                var results = JSON.parse(allCLMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Cell type', 'Effect size Ref', 'Effect size Alt', 'Mean BAD', 'FDR Ref', 'FDR Alt']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row_r = results[i];
					var cell_type = row_r[0];
					var tr = getWidgetTableTr([cell_type, row_r[1], row_r[2], row_r[3], row_r[4], row_r[5]]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}

