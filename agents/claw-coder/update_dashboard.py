# Update the get_phoenix_status function in dashboard.py
# Replace with this version:

def get_phoenix_status():
    """Get actual PhoenixPME status from data collector"""
    metrics = {
        'crf_balance': '0.00',
        'phnx_supply': '0',
        'fee_collected': '0.00',
        'active_escrows': '0',
        'collateral_status': '10% both parties',
        'fee_status': '1.1%',
        'inspection_status': '48 hours'
    }
    
    # Read from data file if it exists
    data_file = Path('/home/greg/dev/claw-coder/phoenix_data.json')
    if data_file.exists():
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                metrics['crf_balance'] = str(data.get('crf_balance', 0))
                metrics['phnx_supply'] = str(data.get('phnx_supply', 0))
                metrics['fee_collected'] = str(data.get('fee_collected', 0))
                metrics['active_escrows'] = str(data.get('active_escrows', 0))
        except:
            pass
    
    return metrics
