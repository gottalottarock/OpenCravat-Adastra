import sys
from pathlib import Path
from copy import deepcopy
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3



class CravatAnnotator(BaseAnnotator):
    def setup(self):
        """
        Set up data sources.
        Cravat will automatically make a connection to
        data/example_annotator.sqlite using the sqlite3 python module. The
        sqlite3.Connection object is stored as self.dbconn, and the
        sqlite3.Cursor object is stored as self.cursor.
        """
        path_to_db = Path(__file__).resolve().parent/'data/adastra.sqlite'
        if not path_to_db.exists():
            print(f"{str(path_to_db)} not exists")
            raise EnvironmentError(f"Database not exists: {str(path_to_db)}")
        self.conn = sqlite3.connect(path_to_db)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()
        self.all_keys_tf = [
            "name",
            "es_ref",
            "es_alt",
            "mean_bad",
            "fdr_ref",
            "fdr_alt",
            "motif_concordance",
        ]
        self.all_keys_cl = [
            "name",
            "es_ref",
            "es_alt",
            "mean_bad",
            "fdr_ref",
            "fdr_alt",
        ]

    def annotate(self, input_data):
        """
        The annotator parent class will call annotate for each line of the
        input file. It takes one positional argument, input_data, and one
        keyword argument, secondary_data.

        input_data is a dictionary containing the data from the current input
        line. The keys depend on what what file is used as the input, which can
        be changed in the module_name.yml file.
        Variant level includes the following keys:
            ('uid', 'chrom', 'pos', 'ref_base', 'alt_base')
        Variant level crx files expand the key set to include:
            ('hugo', 'transcript','so','all_mappings')
        Gene level files include
            ('hugo', 'num_variants', 'so', 'all_so')

        secondary_data is used to allow an annotator to access the output of
        other annotators. It is described in more detail in the CRAVAT
        documentation.

        annotate should return a dictionary with keys matching the column names
        defined in example_annotator.yml. Extra column names will be ignored,
        and absent column names will be filled with None. Check your output
        carefully to ensure that your data is ending up where you intend.
        """
        tf_snps = self._select_tf_snp(input_data)
        cl_snps = self._select_cl_snp(input_data)
        annotations = dict(**tf_snps, **cl_snps)
        print(annotations)
        return annotations

    def _select_tf_snp(self, input_data):
        chrom = input_data["chrom"]
        pos = input_data["pos"]
        alt = input_data["alt_base"]
        q = f"""select
                name, es_ref, es_alt, log_p_value_ref, log_p_value_alt, mean_bad, motif_concordance 
                from tf_snps join transcription_factors  as tf on tf_snps.tf_id=tf.tf_id 
                where tf_snps.chromosome="{chrom}" and tf_snps.position={pos} and tf_snps.alt="{alt}" """
        self.curs.execute(q)
        records = self.curs.fetchall()
        filtered_records = []
        for record in records:
            print(record)
            filtered_record = self.filter_convert_record(record)
            print(filtered_record)
            if not filtered_record:
                continue
            filtered_records.append(filtered_record)
        if not filtered_records:
            return {}
        records = sorted(filtered_records, key=lambda d: min(d["fdr_ref"], d["fdr_alt"]))
        annotations = {
            "top_5_tf": ";".join([rec["name"] for rec in records][:5]),
            "n_tf_snps": len(records),
            "all_tf": [[r[k] for k in self.all_keys_tf] for r in records],
        }
        print(annotations)
        return annotations

    def _select_cl_snp(self, input_data):
        chrom = input_data["chrom"]
        pos = input_data["pos"]
        alt = input_data["alt_base"]
        q = f"""select
                name, es_ref, es_alt, log_p_value_ref, log_p_value_alt, mean_bad 
                from cl_snps join cell_lines  as cl on cl_snps.cl_id=cl.cl_id 
                where cl_snps.chromosome="{chrom}" and cl_snps.position={pos} and cl_snps.alt="{alt}" """
        self.curs.execute(q)
        records = self.curs.fetchall()

        filtered_records = []
        for record in records:
            print(record)
            filtered_record = self.filter_convert_record(record)
            print(filtered_record)
            if not filtered_record:
                continue
            filtered_records.append(filtered_record)
        if not filtered_records:
            return {}
        records = list(sorted(filtered_records, key=lambda d: min(d["fdr_ref"], d["fdr_alt"])))
        annotations = {
            "top_3_cl": ";".join([rec["name"] for rec in records][:3]),
            "n_cl_snps": len(records),
            "all_cl": [[r[k] for k in self.all_keys_cl] for r in records],
        }
        print(annotations)
        
        return annotations


    def filter_convert_record(self, record):
        record = deepcopy(dict(record))
        fdr_ref = 10 ** (-record.pop("log_p_value_ref"))
        fdr_alt = 10 ** (-record.pop("log_p_value_alt"))
        record["fdr_ref"] = fdr_ref
        record["fdr_alt"] = fdr_alt
        if min(fdr_alt, fdr_ref) > 0.05:
            return None
        return {
            k: round(v, 2) if isinstance(v, float) else v for k, v in record.items()
        }

    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        self.con.close()


if __name__ == "__main__":
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
