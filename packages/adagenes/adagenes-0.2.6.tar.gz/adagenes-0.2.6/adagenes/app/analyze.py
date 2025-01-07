import os, datetime
import adagenes as ag
import onkopus as op

from adagenes.app import generate_dataframe_from_dict

sample_file = "/hg38_somaticMutations.l520.GRCh38.vcf"

def recognize_column_types(list):
    column_type = None
    consistent_type = None

    for value in list:

        if value is None:
            continue
        elif value == "":
            continue

        try:
            val = int(value)
            column_type = 'integer'
            continue
        except:
            pass

        try:
            val = float(value)
            column_type = 'float'
            continue
        except:
            pass

        column_type = 'string'

        if column_type is not None:
            if column_type != consistent_type:
                if (column_type=="integer") and (consistent_type == "float"):
                    column_type = "float"
                elif ((column_type == "integer") or (column_type == "float")) and (consistent_type == "string"):
                    column_type = "string"

        consistent_type = column_type

    return column_type


def find_newest_file(directory):
    """
    Find the newest file in the given directory.
    """
    try:
        # List all files in the directory
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f))]

        if not files:
            print("No files found in the directory.")
            return None

        # Find the newest file based on modification time
        #print("FILES ",files)
        #for file in files:
        #    print(os.path.basename(file))
        filtered_files = [file for file in files if os.path.basename(file) != 'log.txt']
        newest_file = max(filtered_files, key=os.path.getmtime)

        print(f"Newest file: {newest_file}")
        return newest_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_file(qid, data_dir, start_row=None, end_row=None):
    """

    :param qid:
    :param data_dir:
    :return:
    """
    data_dir = data_dir + "/" + qid
    #files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    #infile = data_dir + "/" + files[0]
    #print("data dir ",data_dir)
    infile = find_newest_file(data_dir)
    if qid == "sample":
        infile = data_dir + sample_file
    print("load file ",infile)

    bframe = ag.read_file(infile, start_row=start_row, end_row=end_row)
    #print(bframe.data)

    return bframe


def get_column_defs(output_format):
    pass


def get_magic_obj(key, genome_version):
    if key == "clinvar":
        return op.ClinVarClient(genome_version=genome_version)
    elif key == 'protein':
        return op.UTAAdapterClient(genome_version=genome_version)
    elif key == 'transcripts':
        return op.GENCODEGenomicClient(genome_version=genome_version)
    elif key == 'dbsnp':
        return op.DBSNPClient(genome_version=genome_version)
    elif key == 'patho':
        return op.DBNSFPClient(genome_version=genome_version)
    elif key == 'molecular':
        return op.MolecularFeaturesClient(genome_version=genome_version)
    elif key == 'proteinfeatures':
        return op.ProteinFeatureClient(genome_version=genome_version)
    elif key == 'geneexpression':
        return op.ProteinFeatureClient(genome_version=genome_version)
    elif key == 'proteinseq':
        return op.UTAAdapterProteinSequenceClient(genome_version=genome_version)
    elif key == 'functionalregions':
        return op.GENCODEClient(genome_version=genome_version)
    elif key == 'drug-gene-interactions':
        return op.DGIdbClient(genome_version=genome_version)
    elif key == 'clinical-evidence':
        return op.ClinSigClient(genome_version=genome_version)
    elif key == 'filter_text':
        return ag.TextFilter()
    elif key == 'filter_number':
        return ag.NumberFilter()
    else:
        return None


def split_filename(input_string):
    if '.ann.' in input_string:
        return input_string.split('.ann.')[0]
    else:
        return input_string


def append_to_file(filepath, string_to_append):
    try:
        with open(filepath, 'a') as file:
            file.write(string_to_append)
        print(f"String appended to {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


def load_log_actions(logfile):
        if not os.path.isfile(logfile):
            return []

        try:
            with open(logfile, 'r') as file:
                lines = file.readlines()

            processed_lines = []
            for line in lines:
                line = line.split("(")[0]
                processed_lines.append(line)

            return processed_lines
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


def annotate_qid(qid, annotations, genome_version=None, data_dir=None, output_format='vcf'):
    """
    Annotate variant data with selected filters, and stores the annotated data in a new file

    :param qid:
    :param annotations:
    :param genome_version:
    :param data_dir:
    :param output_format:
    :return:
    """

    annotation_requirements = {
        "transcripts": ["protein"]
    }

    print("Annotations ",annotations)
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    for key in annotations.keys():
        if annotations[key]:
            print("Annotate: ", key, " ", qid)


            infile = find_newest_file(data_dir)
            if qid == "sample":
                infile= data_dir + sample_file

            #infile = split_filename(infile)
            infile_name = split_filename(infile)

            previous_actions = load_log_actions(logfile)
            print("loaded logfile ",logfile)
            print("previous actions: ",previous_actions)

            annotation_key = 'Annotation:'+key
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            if contains_substring is False:
                datetime_str = str(datetime.datetime.now())
                print("infile ",infile)
                outfile = infile_name + ".ann."  + datetime_str + "." + output_format

                magic_obj = get_magic_obj(key, genome_version)
                ag.process_file(infile, outfile, magic_obj)

                append_to_file(logfile, annotation_key + "(" + datetime_str + ")" + '\n')

                print("File annotated: ",outfile)
            else:
                print("Annotation already found: ",annotation_key)


    # Generate new column definitions:
    #, cellClass: "rag-blue"


def liftover_annotation(qid, genome_version, output_genome_version, data_dir=None, output_format='vcf'):
    """

    :param output_format:
    :param data_dir:
    :param qid:
    :param genome_version:
    :param output_genome_version:
    :return:
    """
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    infile = find_newest_file(data_dir)
    if qid == "sample":
        infile = data_dir + sample_file

    infile_name = split_filename(infile)
    datetime_str = str(datetime.datetime.now())
    outfile = infile_name + ".ann." + datetime_str + "." + output_format

    magic_obj = ag.LiftoverAnnotationClient(genome_version = genome_version, target_genome=output_genome_version)
    #print("liftover annotation: ",genome_version," to ", output_genome_version,": ",infile, ": ",outfile)
    ag.process_file(infile, outfile, magic_obj)

    annotation_key = 'Liftover annotation:' + genome_version + " to " + output_genome_version + "(" + datetime_str + ")"
    append_to_file(logfile, annotation_key + '\n')


def liftover(qid, genome_version, output_genome_version, data_dir=None, output_format='vcf'):
    """

    :param output_format:
    :param data_dir:
    :param qid:
    :param genome_version:
    :param output_genome_version:
    :return:
    """
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    infile = find_newest_file(data_dir)
    if qid == "sample":
        infile = data_dir + sample_file

    infile = split_filename(infile)
    datetime_str = str(datetime.datetime.now())
    outfile = infile + ".ann." + datetime_str + "." + output_format

    magic_obj = ag.LiftoverClient(genome_version = genome_version, target_genome=output_genome_version)
    print("liftover: ",genome_version," to ", output_genome_version,": ",infile, ": ",outfile)
    ag.process_file(infile, outfile, magic_obj)

    annotation_key = 'Liftover:' + genome_version + " to " + output_genome_version + "(" + datetime_str + ")"
    append_to_file(logfile, annotation_key + '\n')


def apply_filters(qid, filter_model, data_dir=None, output_format='vcf', genome_version=None):
    """
        Apply AG Grid filterModel to the dataset.

        :param data
        :param filter_model
    """
    print("Filters: ",filter_model)
    #bframe = load_file(qid, data_dir)
    #data = bframe.data
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    for column, filter_data in filter_model.items():
        filter_type = filter_data.get("filterType")

        #data_dir = data_dir + "/" + qid
        #print("data dir ",data_dir)
        infile = find_newest_file(data_dir)
        if qid == "sample":
            infile = data_dir + sample_file

        print("Filter: ", filter_type, " ", qid, ": ",infile)
        infile_name = split_filename(infile)

        previous_actions = load_log_actions(logfile)
        #print("loaded logfile ", logfile)
        print("previous actions: ", previous_actions)


        magic_obj = get_magic_obj("filter_" + filter_type, None)
        filter = []
        filter_value = filter_data["filter"]
        filter.append(column)
        filter.append(filter_value)
        filter_type = filter_data['type']
        filter.append(filter_type)
        annotation_key = 'Filter:' + str(filter) #+ "(" + datetime_str + ")"

        if annotation_key not in previous_actions:
            datetime_str = str(datetime.datetime.now())
            print("infile ", infile)
            outfile = infile_name + ".ann." + datetime_str + "." + output_format
            datetime_str = str(datetime.datetime.now())
            #outfile = infile + datetime_str + "_" + ".ann." + output_format
            annotation_key = annotation_key + "(" + datetime_str + ")"

            magic_obj.filter = filter
            print(magic_obj.filter)
            ag.process_file(infile, outfile, magic_obj)
            print("Filtered file: ", outfile)

            append_to_file(logfile, annotation_key + '\n')
        else:
            print("Filter already found: ",annotation_key)


        #if filter_type == "text":
        #    data = [
        #        row
        #        for row in data
        #        if str(filter_data["filter"]).lower() in str(row[column]).lower()
        #    ]
        #elif filter_type == "number":
        #    filter_value = filter_data["filter"]
        #    if filter_data["type"] == "equals":
        #        data = [row for row in data if row[column] == filter_value]
        #    elif filter_data["type"] == "greaterThan":
        #        data = [row for row in data if row[column] > filter_value]
        #    elif filter_data["type"] == "lessThan":
        #        data = [row for row in data if row[column] < filter_value]
    #return data


def apply_sorting(qid, sort_model, data_dir=None):
    """
    Apply AG Grid sortModel to the dataset.

    :param data:
    :param sort_model:
    """
    #print("Sort: ",sort_model)

    bframe = load_file(qid, data_dir)
    data = bframe.data
    data = generate_dataframe_from_dict(data)

    if sort_model:
        for sort in reversed(sort_model):  # AG Grid supports multi-column sorting
            if sort["sort"] is not None:


                #print("Order: ", data)
                column = sort["colId"]
                order = sort["sort"]
                reverse = order == "desc"
                #data.sort(key=lambda x: x[column], reverse=reverse)
                #data.sort(key=lambda x: (math.isnan(x[column]) if isinstance(x[column], float) else False, x[column]),
                #          reverse=reverse)
                data.sort(key=lambda x: (x.get(column, None) is None, x.get(column, None)), reverse=reverse)
    return data


def generate_table_data_from_bframe(bframe, output_format=None):
    column_defs = []
    table_data = []

    if output_format == "vcf":
        table_data = []

        columns = ['CHROM', 'POS','ID','REF','ALT','QUAL','FILTER']
        column_defs = [
            {'headerName': 'CHROM', 'field': 'chrom', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'POS', 'field': 'pos', 'filter': "agNumberColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'ID', 'field': 'id', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'REF', 'field': 'ref', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'ALT', 'field': 'alt', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'QUAL', 'field': 'qual', 'filter': 'agNumberColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'FILTER', 'field': 'filter', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200}
        ]

        for var in bframe.data.keys():
            # base VCF columns
            if "variant_data" in bframe.data[var]:
                if "ID" in bframe.data[var]["variant_data"]:
                    id_data = bframe.data[var]["variant_data"]['ID']
                else:
                    id_data = "."

                if "QUAL" in bframe.data[var]["variant_data"]:
                    qual_data = bframe.data[var]['variant_data']['QUAL']
                else:
                    qual_data = '.'

                if "FILTER" in bframe.data[var]["variant_data"]:
                    filter_data = bframe.data[var]['variant_data']['FILTER']
                else:
                    filter_data = '.'

            #print(bframe.data[var])

            dc = {
                'chrom': bframe.data[var]["variant_data"]["CHROM"],
                'pos': bframe.data[var]["variant_data"]["POS"],
                'id': id_data,
                'ref': bframe.data[var]["variant_data"]["REF"],
                'alt': bframe.data[var]["variant_data"]["ALT"],
                'qual': qual_data,
                'filter': filter_data
            }

            # Preexisting features
            #print(bframe.data)
            info_features = bframe.data[var]["info_features"].keys()
            #print("INFO Features ",info_features)
            #print(bframe.data[var]["info_features"])
            for inf in info_features:
                column_type = recognize_column_types([bframe.data[var]["info_features"][inf]])
                if column_type == "float":
                    filter_type = "agNumberColumnFilter"
                elif column_type == "integer":
                    filter_type = "agNumberColumnFilter"
                else:
                    filter_type = "agTextColumnFilter"

                dc[inf.lower()] = bframe.data[var]["info_features"][inf]

                inf_column = { 'headerName': inf, 'field': inf.lower(), 'filter': filter_type, 'floatingFilter': 'true',
                               'minWidth': 200}

                if inf not in columns:
                    column_defs.append(inf_column)
                    columns.append(inf)

            table_data.append(dc)
        print("Columns ",columns)

    else:

        table_data = [
            {'id': 1, 'name': 'John Doe', 'age': 28, 'country': 'USA'},
            {'id': 2, 'name': 'Jane Smith', 'age': 34, 'country': 'Canada'},
            {'id': 3, 'name': 'Sam Green', 'age': 45, 'country': 'UK'},
        ]

        column_defs = [
            {'headerName': 'ID', 'field': 'id', 'minWidth': 200},
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Country', 'field': 'country'},
        ]

    return column_defs, table_data


def analyze_uploaded_file(qid, data_dir = None,
                          start_row=None, end_row=None,
                          genome_version="hg38",
                          output_genome_version='',
                          output_format="vcf", annotate=None,
                          sort_model=None, filter_model = None):
    """

    :param qid:
    :param data_dir:
    :param genome_version:
    :param output_format:
    :return:
    """

    # Liftover annotation
    if genome_version != "hg38":
        # test if newest file is hg38
        #data_dir = data_dir + "/" + qid
        infile = find_newest_file(data_dir + "/" + qid)
        newest_file_genome_version = infile.split("_")[0].split("/")[-1]

        #print("newest genome version: ",newest_file_genome_version)

        if (newest_file_genome_version == "hg19") or (newest_file_genome_version == "t2t"):
            logfile = data_dir + '/qid' + '/log.txt'
            previous_actions = load_log_actions(logfile)
            annotation_key = 'Liftover annotation:' + newest_file_genome_version + " to hg38"
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            #print(logfile,"::",annotation_key,"::",previous_actions)
            #print("contains ",str(contains_substring))
            if contains_substring is False:
                print("automated liftover annotation:", newest_file_genome_version + " to hg38")
                liftover_annotation(qid, newest_file_genome_version, "hg38", data_dir=data_dir)

    # Liftover
    if (output_genome_version != '') and (output_genome_version != genome_version):
        print("Liftover: ",genome_version," to ",output_genome_version)
        liftover(qid, genome_version, output_genome_version, data_dir=data_dir)

    # Apply filtering
    if filter_model is not None:
        apply_filters(qid, filter_model, data_dir=data_dir)

    # Apply sorting
    if sort_model is not None:
        apply_sorting(qid, sort_model, data_dir=data_dir)

    if annotate is not None:
        annotate_qid(qid, annotate, genome_version=genome_version, data_dir=data_dir)

    # load saved file
    print("load file ",qid," ",data_dir)
    bframe = load_file(qid, data_dir, start_row=start_row, end_row=end_row)
    max_rows = bframe.max_variants


    column_defs, table_data = generate_table_data_from_bframe(bframe, output_format=output_format)


    print("loaded file ", table_data)
    #print("column defs ",column_defs)
    #print("max rows ",max_rows)
    return column_defs, table_data, max_rows

def analyze_search():

    column_defs = []
    table_data = []

    return column_defs, table_data

