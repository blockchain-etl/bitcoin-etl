from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


def get_item_exporter(output):
    if output is not None:
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(output)
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
