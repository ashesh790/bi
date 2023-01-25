function myNewFunction(sel) {
    let sel_value = document.getElementById('property_type').selectedOptions[0].value;
    // alert(sel_value);
    if (sel_value === "agricultureLand") {
        document.getElementById('construction_status_div').style.display = "none";
    }
}
