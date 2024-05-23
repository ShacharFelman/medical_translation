
import "./paragraph-list.css";
import ParagraphListItem from "../list-item";

const ParagraphList = ({textInputs,setTextInputs,onDelete,onTextChange,onOutputTextChange,onClear,translateTextInput}) => {
    const firstElementOnDelete = (index) => {
        if(textInputs.length === 1){
            onClear(index)
        }else{
            setTextInputs([...textInputs.slice(1)]);
        }
        
    }
    return (
        <div className="paragraphs-lists-container">       
            {textInputs.map((text,index)=>{
                return (
                    <ParagraphListItem 
                        id={`paragraph_number_${index}`}
                        textInput={text.input}
                        textInputRawText={text.rawtext}
                        paragraphIndex={index}
                        loading={text.loading}
                        outputText={text.output}
                        onTextInputChange={(value,text) => onTextChange(index,value,text)}
                        onOutputTextChange={(text) => onOutputTextChange(index,text)}
                        key={`paragraph_list_item_index_${index}`}
                        deleteable={index === 0 ? false : true}
                        onDelete={index === 0 ? () => firstElementOnDelete(index) :  () => onDelete(index)}
                        translateTextInput={() => translateTextInput(index)}
                    />
                )
            })}
        </div>
    )
}

export default ParagraphList;