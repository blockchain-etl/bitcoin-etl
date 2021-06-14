from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


def get_item_exporter(output):
    if output is not None:
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping={
                'block': output + '.blocks',
                'transaction': output + '.transactions'
            },
            message_attributes=('item_id',))
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
