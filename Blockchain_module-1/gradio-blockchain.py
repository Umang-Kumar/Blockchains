from blockchain import Blockchain
import gradio as gr

# Create a blockchain instance
blockchain = Blockchain()

# Define a function for displaying the entire blockchain
def display_blockchain():
    if len(blockchain.chain) == 1:
        return 'Blockchain has only the genesis block!'
    blocks = []
    for i, block in enumerate(blockchain.chain):
        block_html = f'''
            <div class="block">
                <div class="block-header">
                    <h3>Block {block['index']}</h3>
                    <p>{block['timestamp']}</p>
                </div>
                <div class="block-body">
                    <p>Data: {block['data']}</p>
                    <p>Proof: {block['proof']}</p>
                    <p>Previous Hash: {block['previous_hash']}</p>
                </div>
            </div>
        '''
        blocks.append(block_html)
        if i < len(blockchain.chain) - 1:
            chain_html = f'''
                <div class="chain-icon">
                    <i class="fas fa-link"></i>
                </div>
            '''
        blocks.append(chain_html)
    blockchain_html = ''.join(blocks)
    return f'''
        <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta2/css/all.min.css">
                <style>
                    .block {{
                        border: 1px solid white;
                        margin: 10px;
                        padding: 10px;
                    }}
                    .block-header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .block-body {{
                        margin-top: 10px;
                    }}
                    .chain-icon {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                </style>
            </head>
            <body>
                {blockchain_html}
            </body>
        </html>
    '''

# Define a function for adding data to the blockchain
def add_data(data):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, data)
    message = f'Data "{data}" has been added to the blockchain!'
    block_html = f'''
        <div class="block">
            <div class="block-header">
                <h3>Block {block['index']}</h3>
                <p>{block['timestamp']}</p>
            </div>
            <div class="block-body">
                <p>Data: {block['data']}</p>
                <p>Proof: {block['proof']}</p>
                <p>Previous Hash: {block['previous_hash']}</p>
            </div>
        </div>
    '''
    return message, block_html

# Create a Gradio interface for adding data to the blockchain
add_data_interface = gr.Interface(
    fn=add_data,
    inputs=gr.components.Textbox(label='Enter data to add to the blockchain:'),
    outputs=[
        gr.components.Textbox(label='Message'), 
        gr.components.HTML(label='Blockchain')
    ],
    title='Add Data to Blockchain',
    allow_flagging="never",
    description='Add data to the blockchain and view the block.'
)

# Create a Gradio interface for displaying the entire blockchain
display_blockchain_interface = gr.Interface(
    fn=display_blockchain,
    inputs=None,
    outputs=gr.components.HTML(label='Blockchain'),
    title='Display Blockchain',
    allow_flagging="never",
    api_name='display_chain',
    description='View the entire blockchain.'
)

# Combine the interfaces using the TabbedInterface
tabbed_interface = gr.TabbedInterface(
    [add_data_interface, display_blockchain_interface],
    tab_names=['Add Data', 'Display Blockchain'],
    title='Blockchain Explorer',
)

# Run the Gradio interface
if __name__ == '__main__':
    tabbed_interface.launch()
