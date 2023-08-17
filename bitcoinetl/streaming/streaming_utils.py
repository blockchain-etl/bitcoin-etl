from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


def get_item_exporter(output):

    item_exporter_type = determine_item_exporter_type(output)
    if item_exporter_type == ItemExporterType.PUBSUB:
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
    
    elif item_exporter_type == ItemExporterType.KAFKA:
        from blockchainetl.jobs.exporters.kafka_exporter import KafkaItemExporter
        item_exporter = KafkaItemExporter(output, item_type_to_topic_mapping={
            'block': 'blocks',
            'transaction': 'transactions',
        })
    else:
        raise ValueError('Unable to determine item exporter type for output ' + output)
    
    return item_exporter


def determine_item_exporter_type(output):
    if output is not None and output.startswith('projects'):
        return ItemExporterType.PUBSUB
    if output is not None and output.startswith('kafka'):
        return ItemExporterType.KAFKA
    else:
        return ItemExporterType.UNKNOWN


class ItemExporterType:
    PUBSUB = 'pubsub'
    KAFKA = 'kafka'
    UNKNOWN = 'unknown'